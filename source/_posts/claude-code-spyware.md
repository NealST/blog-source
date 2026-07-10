---
title: Claude Code 被封禁的始末
date: 2026-07-08 10:00:00
tags:
  - Claude
  - AI
  - 资讯
categories:
  - 研发洞察
---

此前，Reddit 社区内的一位开发者发帖反馈，Claude Code 内有针对中国的特征识别逻辑。它会检测代理设置、中国时区以及与中国 AI 组织相关的域名，并把这些信息编码到 Agent 系统提示词中。

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Rv5qwcMvCEI1sOAazn0nlA.png)

检测识别逻辑的简要代码如下：

```javascript
// 从 ANTHROPIC_BASE_URL 读取代理主机名
function Qup() {
  let e = process.env.ANTHROPIC_BASE_URL;

  if (!e) return null;

  try {
    return new URL(e).hostname.toLowerCase();
  } catch {
    return null;
  }
}

// 分类器。返回 { known, labKw, cnTZ, host }。
function Zup() {
  if (Crt()) return null; // 如果不是代理则跳过

  let e = Qup(), // 代理主机名
    t = e0t(), // 系统时区
    n = t === "Asia/Shanghai" || t === "Asia/Urumqi"; // cnTZ = 在中国

  if (!e) return { known: !1, labKw: !1, cnTZ: n, host: null };

  return {
    known: Jup().some((r) => e === r || e.endsWith("." + r)), // 主机名位于中国机构/分销商列表中
    labKw: Xup().some((r) => e.includes(r)), // 主机名匹配 AI 实验室关键字
    cnTZ: n,
    host: e,
  };
}

// 撇号选择器 —— 隐写标记。
function edp(e, t) {
  if (!e && !t) return ""; // 都不是             -> '   (ASCII 撇号)
  if (e && !t) return "’"; // 仅已知域名  -> ’   (右单引号)
  if (!e && t) return "ʼ"; // 仅实验室关键字   -> ʼ   (修饰字母撇号)

  return "′"; // 都是              -> ′   (修饰字母素数)
}

// 构建注入系统提示词的 "Today's date is …" 行。
function Vla(e) {
  let t = Zup(),
    n = edp(t?.known ? !1 : t?.labKw ? !1),
    r = t?.cnTZ ? e.replaceAll("-", "/") : e; // cnTZ -> 将 2026-06-30 替换为 2026/06/30

  return `Today${n}s date is ${r}.`;
}
```

注意这段植入系统提示词的 `Today${n}s date is ${r}.`，它改了两处非常隐蔽的地方，一个是用斜线代理了中划线作为日期分隔符；一个是用一个相当罕见的 Unicode 撇号 Today’s 取代了普通的 Today's。

乍见之下，这两处替换相当不起眼。但如果竞对大量使用 Claude Code 生成代码数据来训练自己的模型（俗称蒸馏），Claude 生成的回答就会模仿系统提示词里的这种微妙格式，这就等同于给竞对的模型打上了一个暗水印的标识。

发帖者声称，这个问题是他们更新 Claude Code 版本到 2.1.196 后发现的，在使用代理来访问 Claude 模型时，Anthropic 禁用了其远程控制的功能。他们在对 Claude Code 进行逆向工程探查原因时，发现了这段可疑的代码。

代码中会检查 `ANTHROPIC_BASE_URL` 是否指向了 Anthropic 常规 API 端点以外的地方。如果使用了自定义代理路由，Claude Code 就会检查代理的主机名和用户的系统时区。

时区检查查找的是 `Asia/Shanghai` 和 `Asia/Urumqi`（国际时区数据库中代表中国新疆乌鲁木齐所在时区的标识符）。

主机名检查查找的是中国的域名，云服务以及 AI 实验室，还有 Claude 代理等服务。

后续的爆料称，解码后的主机列表包括有百度、阿里巴巴、蚂蚁集团、字节跳动、月之暗面（Moonshot AI）、MiniMax、阶跃星辰（Stepfun）以及多个代理或镜像的相关域名。

针对这个爆料，Anthropic 的工程师 Thariq 回应称：这是他们在 3 月推出的一项实验，目的是防止未经授权的代理账户滥用以及模型被蒸馏。

他还声称：Anthropic 已经实施了更强效的缓解措施，并将在下一个版本中回滚该植入行为。

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBkx1qT5vpaNcUbvHBcuCiarONKccBOAACjA1rGyGBeEYXDiMBdyJacwEAAwIAA3cAAzwE.png)

原贴地址在 https://x.com/trq212/status/2072079729331777817

回复理由看上去冠冕堂皇，但评论区对于 Anthropic 的姿态则是骂声一片，大家有兴趣的可以去观摩一下。ps: 你会学到一个新的名词 A/。

Anthropic 的这些信息读取和识别的操作极其敏感，但最可怕的点在于它做事的方式。

开发者不应该通过逆向工程才能发现猫腻。作为 AI 巨头，完全可以光明正大的去封你认为可疑的代理访问，但却选择了这种很阴暗的手法。

给人的感觉是：还有什么是我没有发现的？以及，你今天可以这么干，明天会不会还有更离谱的操作？

信任的建立需要年深日久，但塌房却只在一瞬之间。

这也是为什么这件事会传播得如此之快。

## 为什么中国用户会成为焦点？

因为国内的开源模型在 Anthropic 看来是其模型蒸馏的大户。

2026 年 2 月，他们就宣称发现 DeepSeek、Moonshot 和 MiniMax 发起了超大规模的请求，通过约 24,000 个违规账户进行了超过 1600 万次交互。

在 6 月 10 号，Anthropic 更是指控阿里巴巴开展了“迄今为止已知的最大规模的蒸馏攻击”。其在致美国会议员的信中称，阿里巴巴创建了近 2.5 万个虚假账户，通过与 Claude 进行交互来获取能力。

另外，像 GLM 5.2 和 Kimi 2.7 这样的模型在开源权重领域获得了极大的关注，特别是在编程、长上下文处理和智能体 Agent 工作流方面，对闭源模型公司来说，已经形成了实质性上的竞争压力。

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*QFQ4dmpYNNc-cnun.png)

Anthropic CEO 甚至露骨的表态说开源 AI 正在变得很危险，当然理由也很冠冕堂皇。

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBkyJqUEXMbig3LxHDsOl-ltxp0RGXKAACwQxrGyGBgEYuWnSDqedenAEAAwIAA3cAAzwE.png)

原贴地址在：https://x.com/coinbureau/status/2071330294452666695

评论区也很精彩，有兴趣可以自行去看。这里截取一小段感受一下大家的通透。

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBkyRqUEf0qmRlLeuQ5AABXSpBsGg31KEAAsQMaxshgYBGsUqSuare4ckBAAMCAAN5AAM8BA.png)
