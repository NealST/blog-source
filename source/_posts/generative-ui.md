---
title: 生成式 UI 的三种范式以及为什么我们需要 MCP Apps
date: 2026-02-21 18:00:00
tags: ["AI", "Front-end-engineering", "React"]
---

AI Agent 在推理和规划方面已经变得越来越强大，但在 UI 层却基本停滞不前，这在很大程度上限制了用户体验。当前围绕于 Agent 的实践更多聚焦于工作流编排和工具技能的实现，在用户体验上仍然依赖于聊天界面，即使任务明显需要表单、预览、控制面板或分步反馈，agent 无法让用户直接进行这种任务交互，带来的常见问题包括：
- 工具执行和进度隐藏在聊天消息背后
- 用户输入模糊，容易被误解，且难以验证
- 多步流程感觉不透明，导致用户不信任结果

于是，生成式 UI 应运而生。

## 什么是生成式 UI？

生成式 UI（有时称为 GenUI）是一种模式，在这种模式下，用户界面的部分内容由 AI Agent 在运行时生成、选择或控制，而不是由开发者完全预先定义。

UI 不是预先硬编码每一个按钮、表单或面板，而是根据用户的需求和上下文动态创建的。Agent 可以决定显示什么 UI、需要从用户那里获取什么输入，以及随着任务的进展状态应该如何更新。

Agent 不仅仅是生成文本，它还可以：
- 收集结构化、经过验证的输入
- 在确切需要时渲染特定于任务的 UI
- 将进度和中间结果显示为真实的 UI
- 随着计划的演变调整界面

这使得 UI 成为 Agent 执行的活跃部分，而不仅仅是聊天框周围的静态包装器，agent 不再需要从文本中推断意图。在用户感知和体验层面，Agent 系统变得更容易理解且更具引导性，用户不再是与一个黑盒交互，而是与一个通过 UI 暴露其状态的系统交互。

**生成式 UI = LLM 输出 → 实时、交互式的 UI**

**示例：**
- 一个旅行查询 → 行程卡片 + 地图 + 可展开的部分
- 一个比较查询 → 可排序的表格

生成式 UI 目前主要有三种范式，主要通过诸如 A2UI、Open-JSON-UI 或 MCP Apps 等 UI 规范来实现。

## 生成式 UI 的三种范式

大多数生成式 UI 实现可以归入三种模式。区分它们的是前端保留了多少控制权，以及赋予了 Agent 多少自由度。

> 下述代码示例均以 copilotKit（一个基于React的开源框架，开发者可以通过极简代码将智能助手深度集成到 Web 应用中） 作为技术实现。

### 静态生成式 UI

静态生成式 UI 是约束最强的模式。

开发者预先构建 UI 组件，Agent 的角色仅限于决定何时出现某个组件以及它接收什么数据。布局和交互完全由应用程序拥有。

以 CopilotKit 中实现一个天气展示的卡片为例，这种模式使用 `useFrontendTool` Hook 实现，它将预定义的 UI 组件绑定到操作的生命周期。

```javascript
// Weather tool - 一个可调用的工具，在样式化卡片中显示天气数据
useFrontendTool({
  name: "get_weather",
  description: "获取某个位置的当前天气信息",
  parameters: z.object({ location: z.string().describe("要获取天气的城市或位置") }),
  handler: async ({ location }) => {
    await new Promise((r) => setTimeout(r, 500));
    return getMockWeather(location);
  },
  render: ({ status, args, result }) => {
    if (status === "inProgress" || status === "executing") {
      return <WeatherLoadingState location={args?.location} />;
    }
    if (status === "complete" && result) {
      const data = JSON.parse(result) as WeatherData;
      return (
        <WeatherCard
          location={data.location}
          temperature={data.temperature}
          conditions={data.conditions}
          humidity={data.humidity}
          windSpeed={data.windSpeed}
        />
      );
    }
    return <></>;
  },
});
```

`useFrontendTool` Hook 允许应用程序注册 `get_weather` 工具，并将预定义的 React 渲染器附加到其生命周期的每个阶段。展示效果：

![](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Futfvm28l3sqrblzuquw2.png)

Agent 可以调用该工具并流式传输参数，但它永远不会控制布局或发明 UI。

### 声明式生成式 UI

声明式生成式 UI 介于静态和完全开放式方法之间。

Agent 不选择预定义的组件，而是返回一个结构化的 UI 描述。这个描述定义了卡片、列表、表单或小部件等内容，然后由前端渲染它们。

这里使用的两个常见的声明式规范是：
1. **A2UI** → 来自 Google 的声明式生成式 UI 规范，基于 JSONL，Agent 可以使用它在响应中返回 UI 小部件。
2. **Open‑JSON‑UI** → OpenAI 内部声明式生成式 UI schema 的开放标准化。

两者都为 Agent 定义了结构化的、与平台无关的方式来用 JSON 描述 UI。

你可以使用 [A2UI Composer](https://a2ui-composer.ag-ui.com/) 为你生成规范，而不是手工编写 A2UI JSON。复制输出并将其粘贴到 Agent 的提示词中作为参考模板。
![](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F1t1yvtk2r1sixyg26njt.png)
![](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fc1trcbzm894v5eq3vtpk.png)

然后在 `prompt_builder.py` 中，挑选一个具有代表性的 A2UI 模板（例如，一个简单的表单或列表）。这就是 Agent 学习输出的内容：

```python
UI_EXAMPLES = """
---BEGIN FORM_EXAMPLE---
[
  { "beginRendering": { "surfaceId": "form-surface", "root": "form-column",
                        "styles": { "primaryColor": "#9B8AFF", "font": "Plus Jakarta Sans" } } },
  { "surfaceUpdate": {
      "surfaceId": "form-surface",
      "components": [
        { "id": "form-column", "component": { "Column": {
            "children": { "explicitList": ["form-title", "name-field", "submit-button"] }
        } } },
        { "id": "form-title", "component": { "Text": {
            "usageHint": "h2", "text": { "literalString": "Contact Us" }
        } } },
        { "id": "name-field", "component": { "TextField": {
            "label": { "literalString": "Your Name" },
            "text": { "path": "name" },
            "textFieldType": "shortText"
        } } },
        { "id": "submit-button", "component": { "Button": {
            "child": "submit-text", "primary": true,
            "action": { "name": "submit_form", "context": [
              { "key": "name", "value": { "path": "name" } }
            ] }
        } } },
        { "id": "submit-text", "component": { "Text": {
            "text": { "literalString": "Send Message" }
        } } }
      ]
    }
  },
  { "dataModelUpdate": {
      "surfaceId": "form-surface", "path": "/", "contents": [
        { "key": "name", "valueString": "" }
      ]
    }
  }
]
---END FORM_EXAMPLE---
"""
```

这个单一的 JSONL 格式块在 A2UI 中定义了一个“联系我们”表单。你将其提供给 Agent，以便它学习 A2UI 期望的三个消息包：`surfaceUpdate`（组件）、`dataModelUpdate`（状态），然后是 `beginRendering`（渲染信号）。

然后将 `UI_EXAMPLES` 添加到 Agent 使用的系统提示词中。通过将 `UI_EXAMPLES`（以及 A2UI schema）附加到 Agent 的指令中，你可以确保每当用户请求 UI 时，它都会根据你的模板流式传回有效的 JSON。

最后一步是使用 `createA2UIMessageRenderer`，它接收 Agent 的 A2UI JSON 和你的主题，然后 `renderActivityMessages` 告诉 CopilotKit 在渲染聊天消息时使用它。

```javascript
import { CopilotKitProvider, CopilotSidebar } from "@copilotkitnext/react";
import { createA2UIMessageRenderer } from "@copilotkit/a2ui-renderer";
import { a2uiTheme } from "../theme";

// 使用你的主题实例化一次 A2UI 渲染器
const A2UIRenderer = createA2UIMessageRenderer({ theme: a2uiTheme });

export function A2UIPage({ children }: { children: React.ReactNode }) {
  return (
    <CopilotKitProvider
      runtimeUrl="/api/copilotkit-a2ui"
      renderActivityMessages={[A2UIRenderer]}   // ← 挂载 A2UI 渲染器
      showDevConsole={false}
    >
      {children}
      <CopilotSidebar defaultOpen labels={{ modalHeaderTitle: "A2UI Assistant" }} />
    </CopilotKitProvider>
  );
}
```

输出展示：
![](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F4w2t5bbhe0oo0c63vzit.png)

这种其实就比较类似于那种低代码协议的模式，让 agent 生成原子化的 UI 描述，然后由前端来完成协议解析和渲染。如果你需要比静态 UI 更多的灵活性，同时仍保持清晰的边界和可预测的渲染，这种模式就比较适合。

### 开放式生成式 UI (MCP Apps)

开放式生成式 UI 是最灵活、最强大的。

在这种模式下，Agent 返回一个完整的 UI 表面。这可以是 HTML、iframe 或其他自由格式的内容。前端主要充当一个容器，显示 Agent 提供的任何内容。

这种方法通常与 **MCP Apps** 一起使用，外部应用程序暴露它们自己的 UI，这些 UI 可以嵌入到 Agent 体验中。

传统的 MCP 工具返回文本、图像、资源或结构化数据，宿主将其作为对话的一部分显示。MCP Apps 扩展了这种模式，允许工具在其工具描述中声明对交互式 UI 的引用，宿主会在原地渲染该 UI。

这种方式可能会引入安全和性能问题、不一致的样式，且主要适用于 web 前端技术栈。但对于复杂的工具和丰富的应用程序，这种模式解锁了仅靠静态或声明式 UI 无法实现的功能。

在 CopilotKit 中，通过将 `MCPAppsMiddleware` 附加到 Agent 中来启用 MCP Apps 支持，这允许运行时连接到一个或多个 MCP Apps 服务器。

```typescript
// app/api/copilotkit/route.ts
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { BuiltInAgent } from "@copilotkit/runtime/v2";
import { NextRequest } from "next/server";
import { MCPAppsMiddleware } from "@ag-ui/mcp-apps-middleware";

// 1. 创建 Agent 并添加 MCP Apps 中间件
const agent = new BuiltInAgent({
  model: "openai/gpt-4o",
  prompt: "You are a helpful assistant.",
}).use(
   new MCPAppsMiddleware({
    mcpServers: [
      {
        type: "http",
        url: "http://localhost:3108/mcp",
        serverId: "my-server" // 推荐：稳定的标识符
      },
    ],
  }),
)

// 2. 创建一个服务适配器，如果不相关则为空
const serviceAdapter = new ExperimentalEmptyAdapter();

// 3. 创建运行时并添加 Agent
const runtime = new CopilotRuntime({
  agents: {
    default: agent,
  },
});

// 4. 创建 API 路由
export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
```

## MCP Apps：工具的端到端交付

### 为什么我们需要 MCP Apps？

我们日常的很多工作都是在处理和检查一些具体的产出物（简称工件），例如：
- 审查代码差异（Diffs）
- 检查追踪、日志和时间线
- 查看和确认表格和仪表盘信息
- 批准或编辑真实的工单

如果你强行将这些内容塞进聊天界面，通常只有两种结果：要么是消耗大量 Token 的长篇大论，要么是一个你不太信任的简短摘要。

多 Agent 工作流会让这个问题变得更糟，因为它们会产出成倍的工件。你会迷失在 12 个终端和 20 个浏览器标签页中，因为需求工单、代码 Diff、运行日志、预览环境和 PR 全都散落在不同的地方。

![](https://cdn.builder.io/api/v1/image/assets%2FYJIGb4i01jvw0SRdL5Bt%2Fdd1f009137a046689faf90e77af579ba?format=webp&width=2000)

**MCP Apps 的核心理念是：与其在所有应用中加入聊天机器人，不如将应用直接放入一个统一的聊天中。**

### MCP Apps 是如何工作的？

传统的 MCP 工具返回文本、图像或结构化数据，宿主（Host）将其作为对话的一部分显示。MCP Apps 扩展了这一模式，允许工具在其描述中声明一个交互式 UI 的引用（例如 `ui://` 资源）。

当 LLM 决定调用支持 MCP Apps 的工具时，会发生以下情况：
1. **UI 预加载与资源获取**：宿主从服务器获取 UI 资源（通常是打包好的 HTML、JS 和 CSS）。
2. **沙盒渲染**：宿主通常在对话内部的一个沙盒化 `iframe` 中渲染 HTML。这限制了应用对父页面的访问，确保了安全性。
3. **双向通信**：应用和宿主通过基于 `postMessage` 的 JSON-RPC 协议进行通信。应用可以请求工具调用、发送消息、更新模型的上下文，并从宿主接收数据。

![](https://cdn.builder.io/api/v1/image/assets%2FYJIGb4i01jvw0SRdL5Bt%2F8e093a7f9a054dbf8f8ad4460fd048d1?format=webp&width=2000)

### MCP Apps 的绝佳应用场景

1. **差异审查与批准**：Agent 修改代码后，不再是在聊天中告诉你已经帮你把那个 Bug 修复了，优化了 3 个函数。而是可以渲染一个真实的 Diff UI（文件树、搜索、代码块选择）。你可以像在 GitHub 上审查 PR 一样，清晰地看到每一行修改，然后点击“批准”或“拒绝”。
![](https://cdn.builder.io/api/v1/image/assets%2FYJIGb4i01jvw0SRdL5Bt%2Ff9c3a971fe84446480ad35b2dd2413d8?format=webp&width=2000)
2. **日志和实时指标探索**：渲染一个带有时间线和过滤器的实时流。你可以挑选出重要的片段（例如某个错误类），应用发出该选择，然后 Agent 运行有针对性的工具调用。
3. **配置向导**：当你需要选择大量选项时，聊天可以变成一个包含多选、复选框和文本字段的表单。UI 最终发出一个干净的对象，而不是与模型进行 20 次来回对话。

### 需要注意的“坑”

- **宿主 UX 成为你产品的一部分**：应用无法控制其容器。如果宿主在一个狭窄的面板中渲染视图，应用可能会显得很糟糕。
- **模型看不见 iframe**：Agent 只能看到应用发出的内容（事件、上下文更新、工具结果）。如果你在表单中输入内容但从未点击“提交”，Agent 就无从反应。
![](https://cdn.builder.io/api/v1/image/assets%2FYJIGb4i01jvw0SRdL5Bt%2F6c3d256879d34cc7b2187aff07c5c0df?format=webp&width=2000)
- **往返延迟**：由 UI 触发的工具调用仍然是工具调用。如果每次点击都触发工具调用，UI 会感觉卡顿，因此需要良好的加载动画设计。

MCP Apps 的设计思想其实比较类似于软件工程的交付思路。传统的交付方式是 `api first`, 主要对外暴露接口，而后来进一步演化出端到端的交付，即统一封装好前后端能力一起交付给用户使用。MCP Apps 也是在单一的 MCP server 中加入了 UI 协议的部分。

## 总结

AI Agent 的能力正在飞速进化，但如果交互方式依然停留在纯文本的“聊天框”时代，其潜力将大打折扣。**生成式 UI (Generative UI)** 的出现，正是为了打破这一瓶颈，让 Agent 能够根据任务需求，动态生成最合适的交互界面。

从**静态生成式 UI**（预定义组件，Agent 填数据）到**声明式生成式 UI**（Agent 输出结构化描述，前端渲染），再到最灵活的**开放式生成式 UI (MCP Apps)**（Agent 直接提供完整的交互式应用），我们看到了 UI 控制权在前端与 Agent 之间的不断平衡与演进。

特别是 **MCP Apps**，通过在聊天界面中直接嵌入沙盒化的交互式应用（如代码 Diff 审查、实时日志探索、复杂配置向导），它不仅解决了多 Agent 协同带来的“工件爆炸”问题，更将 AI 助手从一个单纯的“问答机器人”升级为了一个真正的“智能工作区”。

虽然 MCP Apps 目前仍面临宿主 UX 限制、模型视野盲区以及网络延迟等挑战，但它代表了未来 Agent 交互的必然趋势：**让 AI 适应我们的工作方式，而不是让我们去适应 AI 的聊天框。**
