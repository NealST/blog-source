---
title: 自由切换 agent harness：深入理解 UHP 协议与 HarnessRouter
date: 2026-10-25 10:00:00
tags:
  - AI
  - Agent
  - LLM
  - 架构设计
categories:
  - AI
---

Codex、Claude Code、Gemini CLI、OpenHands 这类工具并不仅是大模型的简单外壳。它们各自封装了完整的 Agent 控制循环、工具调用、文件读写与会话状态管理，这类运行环境通常被统称为 **Agent Harness**。在实际工程落地中，每套 harness 的启动方式、流式事件格式、会话恢复机制以及产物交付方式各不相同。如果业务系统需要对接多套 harness，往往必须为每套运行时重复开发一套接入与适配逻辑。

为了解决接入层的重复建设与适配碎片化问题，社区提出了 **UHP 协议（Unified Harness Protocol）**，将任务分发、流式状态、多轮会话以及文件产物等核心行为抽象为统一的 HTTP 交互契约；开源项目 **HarnessRouter** 则是该协议的参考网关实现，让业务系统只需对接一套兼容 OpenAI Responses 的标准接口，即可按需调度并路由至不同的底层 Harness。

本文深入拆解 UHP 协议的设计理念、HarnessRouter 的网关运行机制与部署方式，并客观梳理了其在当前阶段的工程边界与落地考量。

## 什么是 UHP 协议

要理解 UHP 协议，首先需要明确它所服务的对象，也就是它试图标准化的底层环境：**Agent Harness**。

### 1. 什么是 Harness？

这里的 Harness 指的是一套完整的 Agent 运行时环境（Runtime），通常涵盖以下核心组成部分：

- 驱动大模型持续推理、决策和工具调用的控制循环；
- Shell 命令执行、文件增删改查、代码检索等内置基础工具；
- 对外部扩展体系的接入支持，例如 MCP（Model Context Protocol）、Skills 或插件；
- 保存对话历史与文件系统工作目录（Working Directory）的会话状态管理；
- 将执行过程轨迹与最终交付结果返回给调用方的通信机制。

尽管 Codex、Claude Code、OpenHands 等工具都能胜任上述工作，但它们暴露的命令行参数、事件通知格式、会话管理方式以及恢复机制却大相径庭。

在产品研发中直接集成这些工具时，工程难度往往不在于发起第一次指令，而在于后续如何可靠地处理流式进度输出、超时与主动取消、产物回收、失败重试以及跨轮次的上下文恢复。

### 2. 协议如何标准化 Harness：UHP 的契约设计

针对上述各 Harness 之间协议互不通用的问题，UHP 在业务产品与底层的 Agent Harness 之间建立了一层统一的 HTTP 交互契约：

```text
产品或服务  ── UHP/HTTP ──>  UHP Server  ── 实现自定 ──>  Agent Harness
```

协议只约束客户端与服务端之间的交互标准，不强制限制服务端底层的执行技术选型（无论是容器、操作系统子进程、任务队列还是远程 Worker 集群均可）。

为了完整表达 Agent Harness 的能力，UHP 抽象出了以下 6 个核心对象：

- **Harness**：一套可唯一定位的运行时配置实体，由底层运行时（Base Runtime）、默认模型、系统提示词（System Prompt）、Skills、MCP Server、插件以及步数/时间预算等构成；
- **Response**：单次任务交互的输入请求与执行结果；
- **Session**：连续的 Response 序列，共享对话上下文历史与持久化的文件工作目录；
- **File 与 Container**：随任务上传的输入文件，以及 Agent 在执行过程中生成的输出产物；
- **Environment 与 Memory**：可选挂载的只读项目基线环境，以及跨会话持久化的长效记忆；
- **Streaming、Cancellation 与 Error**：标准的流式进度事件、异步任务取消机制，以及结构化、机器可读的错误反馈。

在交互设计上，客户端首次提交任务时无需显式调用建会话接口，服务端会自动隐式创建 Session；当需要继续对话时，客户端只需将上一轮的 `response.id` 作为 `previous_response_id` 随请求传回即可。

这一设计既避免了一次性单轮任务繁琐的建会话步骤，也让多轮长任务的上下文传递保持简洁自然。

在协议版本管理上，UHP 采用基于日期的版本号规则（例如当前规范版本为 `2026-10-19`）。客户端可以通过 HTTP 请求头 `UHP-Version` 指定协议版本，也可以请求 `GET /v1/uhp` 端点查询服务端的当前版本、能力清单及符合性等级（Conformance Level）。

协议定义了 Core、Extended、Full 三个依次递增的规范等级，并配有一套标准化的一致性测试套件。

### 一个最小的协议示例

下面是一条基础的流式任务请求。`input` 为任务描述，`model` 指定模型，`metadata.harness_id` 指定执行该任务的 Harness：

```json
{
  "input": "请用三点概括 README.md",
  "model": "claude-sonnet-4.6",
  "metadata": {
    "harness_id": "chrn_08dae611630d467ab3e67ed792570ae5"
  },
  "stream": true
}
```

将该请求发送至 `POST /v1/responses`。由于启用了 `"stream": true`，服务端会通过 Server-Sent Events（SSE）通道持续推送事件流。每条事件的 `data` 均为独立的 JSON 对象，核心结构如下：

```text
data: {"type":"response.created","sequence_number":0,"response":{"id":"resp_a1b2c3","status":"in_progress"}}

data: {"type":"response.output_text.delta","sequence_number":1,"item_id":"msg_1","output_index":0,"content_index":0,"delta":"第一点"}

data: {"type":"response.completed","sequence_number":2,"response":{"id":"resp_a1b2c3","status":"completed"}}
```

其中 `sequence_number` 从 0 开始严格单调递增，客户端可以借助该字段检测事件流是否存在乱序或丢包。流式响应的最后一条事件会返回完整的 Response 数据对象：

```json
{
  "id": "resp_a1b2c3",
  "object": "response",
  "created_at": 1786400000,
  "status": "completed",
  "error": null,
  "incomplete_details": null,
  "previous_response_id": null,
  "model": "claude-sonnet-4.6",
  "output": [
    {
      "id": "msg_1",
      "type": "message",
      "role": "assistant",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "text": "第一点……\n第二点……\n第三点……",
          "annotations": []
        }
      ]
    }
  ],
  "store": true,
  "usage": {
    "input_tokens": 5120,
    "output_tokens": 240,
    "total_tokens": 5360
  },
  "metadata": {
    "session_id": "hsess7e78"
  }
}
```

若要在后续交互中延续该会话，下一轮请求只需传入 `"previous_response_id": "resp_a1b2c3"`。服务端会自动还原该轮对话的历史上下文与对应的工作目录状态。

在处理任务状态与错误时，需要特别注意以下三点机制：

1. **状态分类清晰**：任务状态不仅包含成功与失败。`in_progress` 表示正在执行；`completed` 表示正常执行完毕；`incomplete` 表示因为达到预设步数上限（`max_step`）或超时（`timeout_seconds`）而终止；`cancelled` 表示被调用方主动取消；只有底层执行发生异常时才会置为 `failed`。
2. **长任务脱钩连接**：客户端的 SSE 连接意外断开并不会导致后台任务终止，任务仍会在服务端继续运行。客户端可通过 `GET /v1/responses/{response_id}` 随时查询最新状态与产物；若确实需要中止任务，必须显式调用取消接口。
3. **区分请求失败与任务失败**：对于参数非法或鉴权错误等“请求级问题”，服务端直接返回 HTTP 4xx/5xx 状态码及统一的 `error` 对象；而当 Harness 或底层模型在执行期间出现异常时，由于请求本身已被正常受理，HTTP 状态码依然为 `200`，但 Response 对象中的 `status` 会被标记为 `failed`，并携带机器可读的 `error` 信息。因此，客户端不能仅依据 HTTP 状态码来判断任务是否执行成功。

### 它与 OpenAI Responses API、MCP 的关系

UHP 的任务接口设计参考并沿用了 OpenAI Responses API 的基础结构。任务统一提交至 `POST /v1/responses`，文本流式事件和响应体结构也尽量复用业界既有规范。

在此基础上，UHP 通过 `metadata` 以及专有对象扩展了 Harness 选型、持久化会话、文件管理、主动取消、Skills 与工具治理等能力。

需要注意，这种兼容并非“完全等价”。在 UHP 体系中，工具调用是由底层 Harness 自主完成并执行的，而非交由 API 客户端回传执行结果。因此标准 Responses API 中的 `tools` 和 `include` 字段在 UHP 规范中虽然被解析接收，但会被静默忽略，并记录于 `metadata.ignored_fields` 中。

UHP 与 MCP 解决的则是完全不同层级的问题：MCP（Model Context Protocol）连接的是 Agent 与外部工具或数据源；而 UHP 连接的是业务应用系统与完整的 Agent Harness。

二者通常协同工作：业务应用通过 UHP 向 HarnessRouter 下发任务，Harness 在沙箱内部运行期间再调用配置好的 MCP 工具来完成具体操作。

## HarnessRouter 的定位与核心概念

简单来说，UHP 是一套通信协议规范，定义了应用该如何调度 Agent Harness；HarnessRouter 则是该协议的开源参考实现，负责执行具体的任务分发与环境管理。UHP 属于开放协议，其他平台和服务同样可以独立实现这套协议。

在 HarnessRouter 中，有两个核心概念需要区分清楚：

- **Harness Base**：指底层的运行时引擎，例如 `codex`、`claude-code` 或 `openhands`；
- **配置好的 Harness（Configured Harness）**：指基于某个基础运行时，固化了特定模型、系统提示词、Skills、MCP Server、工具调用权限与任务预算的具体配置实例，由服务端分配唯一的 `chrn_...` 格式 ID。

应用通常通过 `chrn_...` 标识来选择具体的 Harness。这样一来，同一个底层的 Base 运行时便可以灵活派生出多套权限、定位和行为完全不同的专用 Agent。

HarnessRouter 将多套 Agent Harness 聚合在统一的 UHP API 背后，屏蔽了各运行时的差异。

下图展示了从用户发起操作，到业务后端提交任务，再到 HarnessRouter 调度具体 Harness 并返回结果的完整链路：

![UHP 与 HarnessRouter 的完整调用链](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBuqxq3du8dik3ldQyJDIeJ-U9SzLlCAACCw5rG0uX6EY6qxXKCBItkwEAAwIAA3cAAz0E.png)

通过这套统一接口，业务系统无需再为不同 Harness 分别处理以下问题：

- 选型与配置不同的 harness、模型与模型提供商；
- 启动长任务并对外提供标准化的 SSE 进度流；
- 持久化管理会话上下文、磁盘工作目录与执行快照；
- 任务输入文件的分发与 Agent 生成产物的归集；
- 任务执行取消机制、最大步数限制与超时控制；
- 统一错误分类、重试策略与幂等执行语义；
- 挂载 Skills、MCP Server、外部插件及只读基线环境。

目前 HarnessRouter 已经适配了包括 Codex、Claude Code、Hermes、Pi、DeepSeek Harness、OpenCode、Gemini CLI、Aider、OpenHands、Agent Zero、nanobot 和 ZeroClaw 在内的 26 个主流 harness。

PS：这 26 个适配项代表系统提供了接入基础，但并不意味着所有组合都能在所有模型与 Provider 下稳定工作。选型时建议查阅官方支持矩阵：<https://github.com/HarnessRouter/harnessrouter/blob/main/docs/support-matrix.md>。

项目主要提供两种部署形态：

- **Community Edition（社区版）**：支持私有化自托管，使用自身的 Provider API Key，数据均持久化在本地存储卷中；
- **HarnessRouter Cloud（云托管版）**：官方托管服务，按会话提供独立的虚拟化沙箱环境，自带弹性伸缩与运维能力。

下文将重点介绍可直接私有化部署的 Community Edition。

## HarnessRouter 的实现原理

### 1. 单容器内的三层架构

Community Edition 默认镜像内部包含三个协同工作的核心进程：

![社区版单容器内的三层结构](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBuuFq3rGtA9uJ7gIjS8Nka6Ein1H-zAACDw5rG0uX8EZhD8mySn_VwgEAAwIAA3cAAz0E.png)

在容器对外端口映射中，仅有 Console 的 `3000` 端口暴露到容器外部，Gateway 与 Runner 默认仅监听容器内部的回环网络地址。

- **Console（控制台）**：Web 可视化管理面板，同时兼任 API 的外部反向代理入口。主要用于配置 Provider 凭证、创建与调试 harness、检索历史会话及生成 API Key。
- **Gateway（网关层）**：协议处理与控制核心。负责 UHP/Responses 接口路由、鉴权与 Workspace 权限隔离、harness 配置解析、模型路由、幂等校验、会话管理、任务取消以及产物文件索引。在自托管模式下，元数据持久化存储于 SQLite，大型文本和会话快照存储于文件系统，敏感凭证则由内置的本地 Secret Store 加密管理。
- **Runner（执行层）**：底层环境与进程调度中枢。Runner 封装了不同 harness 的底层启动命令、Provider 环境变量注入规则、上下文恢复方式以及 CLI 标准输出解析逻辑。

### 2. 一次请求的执行全流程

以标准的任务请求 `POST /v1/responses` 为例，内部执行链路包含以下步骤：

1. **鉴权与作用域校验**：Gateway 校验请求头中的 HarnessRouter API Key，确认调用方所属的工作区权限。
2. **配置解析**：Gateway 提取 `metadata.harness_id`，查询对应的基础运行时、模型配置、系统提示词、挂载的 Skills、MCP Server、插件以及步数/时间预算。
3. **会话校验**：若请求携带 `previous_response_id`，Gateway 检索原有 Session，确认继续沿用该 harness（协议约束同一 Session 内不允许并发执行两个任务）。
4. **凭据准备与任务下发**：Gateway 生成当前轮次所需的 Provider 路由与临时凭据，将标准化任务载荷转发至 Runner。
5. **工作目录准备**：Runner 创建或挂载恢复该 Session 专属的工作目录，写入 harness 专属配置文件，并挂载 Skills、插件与只读基线环境。
6. **沙箱进程启动**：Runner 以该 Session 绑定的独立 Unix 系统用户身份启动对应的 Harness CLI。CLI 进程在真实的 POSIX 工作目录内执行 Shell 命令与文件系统读写。
7. **输出捕获与事件标准化**：Runner 实时监听 CLI 的输出流，将其归一化为统一的内部事件流；Gateway 进一步将其映射为 UHP/Responses 的文本增量、Reasoning 摘要、`function_call` 与 `function_call_output` 事件。过程中产生的磁盘文件则通过文件对象与 `container_file_citation` 标注与响应关联。
8. **事件推送**：Gateway 通过 SSE 长连接将标准事件流推向客户端；若为非流式请求，则在内部聚合成最终的 Response 对象后一次性返回。
9. **状态固化与归档**：任务执行完毕后，工作目录生成快照（Checkpoint）；新增文件标记为 Session 产物（Artifact），供后续轮次恢复上下文或下载。

这套架构的核心价值在于：它不是单纯地把 Prompt 转发给大模型，而是将具备复杂状态和本地环境操作能力的 Agent 任务，封装成了稳定可靠的标准后端服务。

### 3. 会话状态与安全隔离

在 UHP 体系中，Session 同时承载了对话历史、工作目录文件以及绑定的 Harness 状态。HarnessRouter 会为每个 Session 分配相互隔离的本地磁盘目录。

在社区版的默认单容器部署中，不同 Session 共享宿主容器与 Runner 实例。为了实现基础安全隔离，Runner 采用针对每个 Session 分配不同 Unix 系统用户的策略，通过操作系统的 POSIX 文件权限机制防止不同会话之间相互越权读取工作目录、数据库、Blob 存储及 Secret Store。

这种机制有效避免了所有 Agent 混用单一 root 或系统账户带来的直接风险，但与全虚拟化的独立容器沙箱相比，其隔离强度仍有本质区别。云托管版采用的是每次会话独享沙箱的机制，两者在安全防范级别和横向扩缩容边界上截然不同。

### 4. Provider 与凭据管理

HarnessRouter 在架构上将“使用哪套 Harness”与“调用哪个模型 Provider”彻底解耦。一个 Harness 配置可以指定默认模型，Gateway 则结合全局配置的 Provider 连接池动态判定该模型是否可用。

UHP 协议明确规定：服务端不得在未声明的情况下静默降级或替换模型；若无法满足请求，必须直接拒绝或在响应元数据中显式记录替换事实。

在 Community Edition 默认的“所有者信任（Owner-Trust）”模式下，使用者完全拥有机器、Agent 运行时与 Provider 密钥，执行任务时所需的凭证会按需注入到运行时环境中。

由于 Agent 本身具备执行任意代码的能力，因此必须将整个部署实例视作一个具备代码执行特权的环境。注入给 Agent 的各类 Token 必须遵循最小权限原则，尽可能采用短期、受限的专用密钥。

## 如何上手使用

### 1. 启动 Community Edition

运行环境需准备 Docker、约 4 GB 可用磁盘空间，以及至少一个可用模型 Provider 的 API Key（镜像本身不内置模型，亦不包含试用调用额度）。

```bash
docker run -d --name harnessrouter \
  -p 127.0.0.1:3000:3000 \
  -v harnessrouter:/data \
  harnessrouter/harnessrouter
```

初次启动时，容器会在后台下载并安装已启用的 Harness CLI。可通过以下命令查看实时启动日志：

```bash
docker logs -f harnessrouter
```

当日志输出 `ready on :3000` 后，在浏览器中访问 <http://localhost:3000>。系统的初始默认用户名和密码均为 `harnessrouter`。首次登录后建议立即修改初始密码；在完成密码修改前，请勿将该服务直接暴露于公网环境中。

系统元数据、上传文件、已安装的 CLI 依赖以及各会话工作目录均持久化保存在名为 `harnessrouter` 的 Docker 数据卷中。单纯拉取新镜像并不会直接覆盖运行中的容器；在进行版本升级时，应先停止旧容器并备份该数据卷，再挂载原数据卷启动新镜像。切勿随意删除该数据卷，亦应避免执行带有 `-v` 参数的 `docker compose down -v` 命令。

### 2. 接入模型并运行第一个任务

进入控制台后，点击左下角账户菜单中的 **Bring your own key** 配置项，填入模型 Provider 的 API Key。随后在 **Start** 页面中输入目标任务指令，系统支持由网关自动推荐适用的 Harness 与模型，也支持手动指定。配置完成后提交请求，控制台将实时展示 Agent 的推理过程、工具调用轨迹以及最终输出文件。

若仅为了验证本地服务部署是否正常，可优先使用控制台内置的录制演示（Recorded Demo）。演示数据在本地回放，不会触发实际的模型 API 调用，只有发起真实的新任务时才会消耗 Provider 额度。

### 3. 从业务后端调用 API

在控制台的 **API Keys** 页面生成专用的 HarnessRouter API Key。该凭据仅用于客户端调用 HarnessRouter 服务端接口，不同于控制台登录密码或上游 Provider 密钥，且必须妥善保存在服务端环境中，避免泄露至前端客户端。

```bash
export HARNESSROUTER_BASE_URL=http://localhost:3000/api/harness
export HARNESSROUTER_API_KEY=你的_HarnessRouter_API_Key

curl --fail-with-body -sS "$HARNESSROUTER_BASE_URL/v1/responses" \
  -H "Authorization: Bearer $HARNESSROUTER_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "input": "请用三点概括 README.md",
    "metadata": {"harness_id": "codex"},
    "model": "gpt-5.4-mini",
    "stream": false
  }'
```

上述示例中的 `codex` 为 HarnessRouter 社区版提供的内置运行时别名。若需调用在控制台预先配置的自定义 Harness，需传入控制台或 `GET /v1/harnesses` 接口返回的标准 `chrn_...` 标识。

具备跨平台兼容性的 UHP 客户端应始终优先使用服务端分配的标准 ID。需要注意，上述 Harness 与模型仅作演示用途，实际调用前须确保对应的 CLI 已安装完毕，且已配置的 Provider 能够正常提供该模型服务。

将 `stream` 设置为 `true` 后，服务端将返回 SSE 事件流。若要在同一会话中继续多轮对话，只需将上一轮返回的 `id` 传入下一轮请求的 `previous_response_id` 字段：

```json
{
  "input": "再补充一条关于部署的说明",
  "previous_response_id": "resp_上一轮返回的ID",
  "metadata": {"harness_id": "codex"},
  "model": "gpt-5.4-mini",
  "stream": true
}
```

针对可能发生网络超时的任务创建请求，可以在请求头中携带 `Idempotency-Key`。携带相同幂等键及相同请求体的重试请求，将直接返回首次执行的结果，避免重复启动底层 Agent；若携带相同幂等键但请求体内容不同，网关将直接返回 HTTP `409` 冲突。

此外，运行中的实例会在 `$HARNESSROUTER_BASE_URL/v1/openapi.json` 提供机器可读的 OpenAPI 契约，并在 `/v1/docs` 提供可视化交互文档。

### 4. 文件的传入与取回

UHP 支持两种文件输入方式：对于小文件，可编码为 Base64 Data URL 直接放入 `input_file.file_data` 字段；对于体积较大的文件，建议先通过 `POST /v1/files` 端点完成上传，再在任务请求中引用返回的 `file_id`。采用后一种方式可有效避免在接口重试时重复上传完整文件数据。

Agent 在执行过程中向工作目录写入的文件会自动归档为该 Session 的产物（Artifact）。服务端的 Response 会在消息的 `annotations` 数组中附带 `container_file_citation` 引用信息，标明 `container_id`、`file_id`、文件名以及下载链接。客户端亦可通过 `GET /v1/sessions/{session_id}/files` 列出当前会话产生的所有文件，再通过 `/v1/containers/{container_id}/files/{file_id}/content` 下载文件原文。

在安全策略上，必须将 Agent 生成的产物视作不可信数据。下载接口须设置明确的 `Content-Type` 响应头，并建议附加 `X-Content-Type-Options: nosniff`；若面向公网用户提供服务，产物下载域名最好与主站域名保持物理隔离，避免 Agent 生成的 HTML 或 JS 脚本引发同源环境下的存储型 XSS 漏洞。

### 5. 正式接入前的小范围验证

在正式接入核心业务流程前，不应仅验证“能否正常回复一句话”，建议至少对以下 6 项典型场景开展回归测试：

- 首轮任务与同一 Session 下多轮长任务的连续交互；
- 会话中途切换模型时的行为是否符合预期；
- 生成、索引及下载大体积文件产物的完整链路；
- 在 Runner 进程或工作目录被系统回收后，旧会话能否无损恢复；
- 发生超时、主动取消、Provider 欠费限流及 MCP 服务宕机时的异常处理表现；
- 网络重试触发幂等机制时，是否能够确保无额外副作用。

官方支持矩阵已针对首轮执行、上下文续接、模型切换、产物交付及回收恢复等核心维度提供了详细评测结果。

在实际工程中，业务任务往往会暴露出通用测试未能覆盖的边缘情况，因此建议在锁定目标 Harness、模型版本及 Provider 组合后，建立专属的自动化回归测试集。

## 当前局限与工程考量

### 1. UHP 规范仍处于 Draft 阶段

目前 UHP 规范文档明确标识为 Draft（草案）。虽然该协议已具备正式的版本管理机制、OpenAPI 契约、JSON Schema 以及一致性测试套件，但在后续演进中仍可能发生调整。

当前版本中仍保留着部分权衡细节（例如任务级字段采用 `snake_case`，而 Harness 级对象采用 `camelCase`；Session 删除操作仍兼容保留了历史别名 `/v1/traces/{id}` 等）。

因此，接入方应主动调用 `GET /v1/uhp` 端点，根据服务端实际声明的能力字段（Capabilities）动态启用特性，而不应盲目假定所有 UHP 服务端均实现了 Full 级别的能力，亦不应将 HarnessRouter 的个别内部实现细节视为协议本身的通用要求。

### 2. “支持 Harness”不等于所有组合均稳定可用

Agent 的最终执行表现由 Harness 引擎、CLI 版本、模型基座、Provider 接口、事件传输格式及具体任务特征共同决定。在实际评测中，同一款模型在某个 CLI 中可以正常调用工具，但在另一个 CLI 中可能仅输出工具调用的纯文本；部分组合可以顺利跑通首轮指令，但在多轮会话恢复或文件输出阶段却频繁失败。

官方支持矩阵详细记录了各组合的通过状态、重试率、模型别名映射以及已知的显式缺陷（例如某些组合未能命中 Prompt Cache，个别 Harness 在任务被取消后无法保留该轮上下文，还有部分轻量 Harness 自身缺乏完备的多步工具控制循环）。在技术选型时，应结合具体表格项与评测用例做严谨评估，而非仅依据首页宣传的支持数量做决策。

### 3. 依赖上游 CLI 动态安装带来的环境漂移

在默认镜像设计中，许多 Harness CLI 是在容器首次启动时由脚本从上游动态下载安装的，并未完全固化在底层镜像层内。上游工具的版本演进、启动参数变更、输出格式调整、模型适配范围乃至开源许可协议的变更，均可能影响运行稳定性。若某一个 backend 下载安装失败，虽然不会阻塞容器启动，但在首次调用该 backend 时会直接报错。

在生产环境中，建议制作完全固化所有依赖的专用镜像，锁定镜像版本并保持持久化数据卷备份，同时在容器启动后校验实际已安装的 backend 列表，并审查各个 CLI 独立的开源协议与服务条款（HarnessRouter 本身采用的 Apache 2.0 协议并不覆盖其所调度的第三方工具）。

### 4. 社区版在隔离强度与资源容量上的明确边界

Community Edition 默认采用单容器、单 Runner 实例架构，通过在单一操作系统内部划分不同的 Unix 用户和独立目录来实现会话隔离，并非为每个会话启动独立的容器沙箱。其实际并发承载上限完全受限于宿主机的 CPU、内存及磁盘 I/O 资源，无法像专业云托管平台那样实现按需动态扩缩容。

更为关键的是，Agent 运行时原生具备执行 Shell、Git 及文件系统读写的能力。系统文件权限虽然能够隔离不同 Session 间的数据越权，但无法防止特权代码执行带来的系统性风险。

因此，绝不能向 Agent 注入超出业务所需的高特权密钥，亦严禁将维持默认初始密码的实例直接暴露在公网中。若需在生产环境中对外部署，必须完成密码修改，前置配置 HTTPS 反向代理，并显式关闭反向代理层的 SSE 响应缓冲。

此外，抓取的网页内容、外部代码仓库、用户上传的文件以及记忆模块注入的数据均属于不可信输入源，UHP 协议层本身无法防御针对大模型的 Prompt 注入攻击（Prompt Injection）。

如果需要处理不可信输入源的任务，就不能与拥有高权限本地工具、敏感凭据或特权 MCP Server 的 Harness 配置共用同一运行环境。

在数据生命周期方面，社区版中未显式删除的数据不会自动过期淘汰。调用 Session 删除接口会立即且永久清除该会话相关的记录、产物与快照文件；单独删除的 harness、response、environment 和 upload 资源通常在保留 30 天后由定时任务清理。由于旧数据备份中仍可能包含已删除的内容，因此在制定数据保留策略时，须将备份轮换与清理策略同步纳入考量。

### 5. Responses API 兼容层的功能边界

UHP 在接口外形上借鉴了 OpenAI Responses API，但并未全量承载其所有语义定义。在当前规范中，`tools` 与 `include` 参数会被解析但静默忽略；针对 `max_output_tokens` 参数，HarnessRouter 虽会接收但会将其标记为 ignored。

这是因为一个完整的 Agent 任务通常包含模型的多轮推理与工具调用，单次输出的 Token 上限无法合理表征整个任务的计算边界，甚至可能意外截断关键的工具调用参数。针对任务级资源预算，应改用 `max_step`（最大步数）与 `timeout_seconds`（超时时长）字段。

若现有的上层 SDK 深度依赖 Responses API 的高级特性，在迁移至 UHP 时必须仔细检查响应头及 `metadata.ignored_fields`，切勿仅凭 HTTP 返回 `200` 就断定所有入参字段均已生效。

### 6. 一致性测试无法替代深层运行时安全校验

UHP 官方提供的一致性测试套件能够通过运行真实任务，有效检验流式传输缓冲、异步取消可靠性、产物路径穿越漏洞以及下载异常等基础工程缺陷。然而，单凭一套标准的测试用例无法全面验证复杂的跨租户多主体对象隔离，亦无法证明所有工具禁用限制均由底层运行时硬性拦截。

协议允许某些轻量 Harness 仅通过系统提示词（System Prompt）指令来弱约束 `disabledTools`，而模型遵循指令不调用工具与底层沙箱硬性拦截工具，在 HTTP 协议层表现出的结果可能完全一致。

若业务场景对某些敏感工具或命令调用存在绝对的合规拦截要求，必须在底层 Harness 的实现层级展开白盒验证，不能单纯依赖 UHP Conformance 认证标签。

## 总结

UHP 协议所解决的是一个非常明确且关键的工程痛点：如何让上层业务产品以统一、可靠的方式调度形态各异的 Agent Harness。

HarnessRouter 则通过落地 Gateway 协议网关、Runner 调度引擎、持久化状态管理以及针对主流 Harness 的深度适配，将这一协议转化为了开箱即用的基础设施。

这套方案尤其适合需要快速评估或在多套 Agent 运行时之间平滑切换，同时希望避免业务后端与特定 CLI 私有接口深度耦合的研发团队。它能够大幅减少接入层的重复工程开销，但并不会抹平大模型和 Harness 本身的底层能力差异。

最为务实的落地策略是：先通过 Community Edition 在私有环境中跑通真实的端到端业务场景，结合官方支持矩阵锁定适合自身业务的基座与工具组合，建立完善的自动化回归、安全权限审查与部署规范，再稳步接入核心生产链路。
