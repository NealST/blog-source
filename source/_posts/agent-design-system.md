---
title: 为什么 Agent 没有遵循你写的 Rules
date: 2026-06-16 10:00:00
tags:
  - Agent
  - Agent Experience
  - 工程效能
categories:
  - 研发洞察
---

前几天，我的一个 Agent 提交了一份修改偏好设置面板的 PR。截图上看实现效果没啥问题：间距精准，标签完整，响应式布局也做了适配。

但是我发现面板代码中用了一个 `components/legacy/` 目录下的弹窗组件，这个目录纯粹是为了维持一些旧页面不崩才留着的。此外，它还调用了一个废弃的表单 Hook。样式上，报错状态的色值直接写死了 `#FF3B30`，完全没走设计 Token。

这并不是模型变蠢了，相反，恰恰说明它充分地“学习”了我的代码库。由于项目里旧代码的数量远超新代码，Agent 在阅读仓库代码后，推算出了我的编码习惯。问题在于它学到的是仓库中的历史包袱，而不是真正的设计规范。

单个 pr 的问题看似不大，但 Agent 生码效率极高，当重复且批量地生产这种问题时，人类是匹配不了 review 节奏的。

那么我们为啥不用 `Agents.md` 这种规则文件来限定 agent 行为呢？

## 为什么长篇大论的 Rules 斗不过历史包袱？

面对这种错误，大部分人的直觉是去写一个详细庞大的规则文件，比如 `.cursorrules`， `Agents.md`。我也尝试过，在规则文件中强调“永远使用语义化 Token”、“禁止引入 legacy 库”、“表单必须按照 xx 方式来实现”等等。

但根本没用，Agent 并不遵循。

因为在 AI 眼里，自然语言打不过现有代码。

背后的逻辑是在上下文中，实际代码比规则指令会吸引更大的注意力。而且，文档本身是落后于代码的，当代码改动后，文档不会自动更新，代码天然就比文档有更高的置信度。

模型在权重上更看重实例。当它要写个新组件时，最直接的做法就是搜个类似的依样画葫芦。如果相邻的几个文件全在写内联的十六进制色值，即使规则文档中声明了“严格使用语义化 Token”，这些内联色值写法还是会占据主导。

简单来说，代码本身就是最大也最权威的 Prompt。

那么，这种问题应该怎么解？

## 靠编译错误重塑 Agent 上下文

直接重构所有老代码显然不可能。

核心的解法是：在局部环境中让错误路径直接抛出异常。

运转逻辑大致如下：

![](https://cdn.builder.io/api/v1/image/assets%2FYJIGb4i01jvw0SRdL5Bt%2F65dc300c81fa479b8b81ccc376da80a3?format=webp&width=2000)

让 Rules 尽可能精简并直接指向代码，让代码来教 Agent 什么是最佳实践，让校验工具施加硬性约束并在报错中触发 Agent 的自我修复。

首先是组件引用问题。

### 1. 强行阻断旧组件

在 Agent 眼里，`components/ui/` 和 `components/legacy/` 只是两个能跑的目录。后者代码多，训练信号还更强。

不用向模型解释二者差别，如果不希望 Agent 使用旧组件，直接把它掐成编译错误：

```json
{
  "rules": {
    "no-restricted-imports": [
      "error",
      {
        "patterns": [
          {
            "group": [
              "@/components/legacy",
              "@/components/legacy/*",
              "**/components/legacy/*"
            ],
            "message": "Do not import legacy UI. Use '@/components/ui' and check 'src/design-system/examples' for current patterns."
          }
        ]
      }
    ]
  }
}
```

上述中 `message` 字段其实是个内置 Prompt，用来告诉 Agent 正确的组件引用方式。

现代的 Coding Agent 都会在后台循环跑 Compiler 和 Linter，Agent 不会忽视这种 Lint Error，它会把报错当成修复指令。

### 2. 用类型切断幻觉

过于宽松的 TypeScript 接口定义会导致 Agent 生成问题代码，比如：

```typescript
// 脆弱：允许无效的属性组合
interface CardProps {
  title: string;
  variant?: "informational" | "interactive" | "marketing";
  href?: string;
  onClick?: () => void;
  badgeText?: string;
}
```

在这个类型定义下，Agent 会生成带有 `onClick` 方法的信息卡片，或者漏掉 `badgeText` 的营销卡片。由于都是可选属性，类型检查全绿，Agent 会认为一切正常。

用可辨识联合类型就可以堵死这种空子：

```typescript
// 严谨：无效状态将直接报错
type InformationalCard = {
  variant: "informational";
  title: string;
};

type InteractiveCard =
  | { variant: "interactive"; title: string; href: string; onClick?: never }
  | { variant: "interactive"; title: string; onClick: () => void; href?: never };

type MarketingCard = {
  variant: "marketing";
  title: string;
  badgeText: string;
};

type CardProps = InformationalCard | InteractiveCard | MarketingCard;
```

现在，当 Agent 试图给信息卡片强加 `badgeText`，TypeScript 编译会直接报错，并反馈给 Agent 的验证循环自动修复。

核心思路是充分利用 typescript 的类型检查能力。

### 3. 没收色值选择权

让 Agent 自己挑颜色，它会凭视觉相似度盲猜，并且不一定会遵循设计 token 的规范定义。

我们可以用 Stylelint 剥夺其选择权。

```json
{
  "plugins": ["stylelint-declaration-strict-value"],
  "rules": {
    "scale-unlimited/declaration-strict-value": [
      ["color", "background-color", "border-color"],
      {
        "ignoreValues": ["inherit", "transparent", "currentColor"],
        "message": "Use semantic color tokens such as var(--color-border-error), not raw values or reference colors."
      }
    ]
  }
}
```

这里思路其实与前述的 eslint 规则相似，通过 stylelint 限定色值只能采用定义好的设计 token。

但前提是项目中的 token 规则已经配置齐全，避免 Agent 在代码里凭空捏造根本不存在的变量名。

### 4. 指定一个北极星目录

模型既然靠示例学习，那就给它找条对的路。

我单独维护了一个 `src/design-system/examples/` 目录，只放置参考实现，包括实际投产的设置表单、数据表格、详情页等。这些组件都能正常编译并在生产环境运行。如果依赖的底层组件一旦发生破坏性 API，持续集成会直接抛异常。

```tsx
// src/design-system/examples/settings-form.tsx
import { useForm } from "react-hook-form";
import { FormField, Input, Button } from "@/components/ui";

interface ProfileFormData {
  email: string;
}

export function SettingsFormExample() {
  const { register, handleSubmit, formState: { isSubmitting, errors } } = useForm<ProfileFormData>();
  
  const onSubmit = async (_data: ProfileFormData) => {
    await new Promise((resolve) => setTimeout(resolve, 1000));
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <FormField label="Email Address" error={errors.email?.message}>
        <Input {...register("email", { required: "Email is required" })} aria-invalid={Boolean(errors.email)} placeholder="you@example.com" />
      </FormField>
      <Button type="submit" loading={isSubmitting}>Save changes</Button>
    </form>
  );
}
```

接下来就可以极限压缩 Rules 文件：

```markdown
# Agent Instructions
- Use UI primitives exclusively from `src/components/ui/`
- For settings interfaces or forms, match the structure of
  `src/design-system/examples/settings-form.tsx`. Do not write custom wrapper forms.
- See `src/design-system/deprecated.md` for old components and their replacements.
```

通过代码来教学，Agent 直接抄作业，所有模型都能做得近乎完美。

而且代码相比文档是更有生命力和实时性的，文档会过期，但代码是实打实在运行的。

## 定义验证循环

在提起 PR 之前，Agent 必须跑通一条指令：`npm run test:verify-ui`。

该指令串联了 TS 编译、ESLint、Stylelint，外加一组跑在后台的 Storybook 交互测试。

```typescript
// src/components/ui/Modal.stories.tsx
export const InteractiveState = {
  play: async ({ canvasElement }: { canvasElement: HTMLElement }) => {
    const canvas = within(canvasElement);
    const trigger = canvas.getByRole("button", { name: /Open Modal/i });
    await userEvent.click(trigger);

    const dialog = await screen.findByRole("dialog");
    await expect(dialog).toBeInTheDocument();

    const input = within(dialog).getByRole("textbox", { name: /Username/i });
    await expect(input).toHaveFocus(); // Agent 此前就会死在这步测试上
  }
};
```

Agent 写的弹窗只要焦点处理有误，本地测试会直接挂掉。报错抛出后，它会自我重构，直到跑通为止。

实操其实远没有想象中那么顺利。模型很聪明，会用各种手段“作弊”通关。比如随手加一句 `eslint-disable` 注释，强行使用 `any` 类型断言，或者干脆把跑不过的测试用例删了。因此除了跑测试，还需要再叠加一层针对 Agent 的“元规则”（Meta-layer）限制：在 Lint 中严禁变更文件来抑制错误，并用 Diff 检查明确标记出被篡改的测试文件。

全绿的通过状态并不代表好的设计，但至少我们可以通过这些工程化的手段避免 Agent 出现一些低级繁琐的错误。

人类可以把注意力集中在关键的业务判断上。

## 写在最后

强类型、Linter、参考实现和交互测试，在 Agent 出现前就已经存在了。

放在以前，这些工程规范属于“Nice-to-have”。对于碳基开发者来说，跳过它们问题不大。因为人类天然拥有默契，能通过口头提醒、Review 评论甚至群聊来吸纳这些隐性知识。

但 Agent 不会，Agent 是完全无状态没有记忆的硅基产物。

这也是 Agent Experience (AX) 的核心所在：**通过修整代码库，让环境变得不言自明且具有强纠偏能力。**

Agent 拥有比人类更强的破窗效应。

一个规范整洁的代码工程对 Agent 来说就是最大的复利。

