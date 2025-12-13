---
title: 重塑 React 开发：现代化 Hooks 最佳实践
date: 2025-12-13 22:34:58
tags: "react"
---

## 前言

React Hooks 问世已有数年，但在日常很多场景和代码库中，我们依然沿用着最初的那套写法：各种 useState 搭配沉重繁杂的 useEffect，然后再加上大量未经深思熟虑就复制粘贴的代码。

**但 Hooks 的初衷不仅仅是生命周期方法的简单替代品。它本质上是一套设计系统，旨在构建更具表现力、更模块化的架构。**

随着 Concurrent React（React 并发模式，即 React 18/19 版本）的到来，React 处理数据（尤其是异步数据）的方式已经发生了根本性转变，比如 React 19 衍生出的服务端组件（Server Components）、use() API、Server Actions 等等。

因此，让我们以此为契机，梳理一下现代 Hooks 的最佳实践，探讨 React 官方所推崇的开发范式，并分析生态系统中反复出现的那些陷阱。

## useEffect 的陷阱：做得太多，调得太频

useEffect 仍然是最常被误用的 Hook。它往往沦为不属于它的逻辑的“垃圾场”，例如数据获取、计算派生值，甚至简单的状态转换。这通常就是组件开始变得“幽灵般不可预测”的时刻：它们会在奇怪的时间点重新渲染，或者渲染次数远超预期。

```typescript
useEffect(() => {
  fetchData();
}, [query]); // 即使 query 的新值在逻辑上等同于旧值，这里也会重新运行
```

这种痛苦大多源于混淆了“派生状态”与“副作用”，而在 React 的模型中，这两者的处理方式截然不同。

## 回归本源：正确使用 Effect

React 对此的规则出奇地简单：
只在处理真正的副作用（即与外部世界交互）时使用 Effect。
其他所有逻辑，都应在渲染期间（Render Phase）通过派生计算完成。

```tsx
const filteredData = useMemo(() => {
  return data.filter(item => item.includes(query));
}, [data, query]);
```

当你确实需要使用 Effect 时，React 的 useEffectEvent（实验性 API）将是你的得力助手。它允许你在 Effect 内部访问最新的 props 或 state，而无需因将它们加入依赖数组而导致 Effect 频繁触发。

```tsx
const handleSave = useEffectEvent(async () => {
  await saveToServer(formData);
});
```

在伸手使用 useEffect 之前，请先自问：
* 这是由外部因素（网络、DOM、订阅）驱动的吗？
* 还是我可以仅在渲染过程中计算出这个结果？
如果是后者，使用 useMemo、useCallback 或框架提供的原语会让你的组件更加稳健。

🙋🏻‍♂️ 提示
不要把 useEffectEvent 当作是规避依赖数组检查的“作弊码”。它专门为了优化 Effect 内部的逻辑执行而设计。

## 自定义 Hooks：不止于复用，更在于封装

自定义 Hooks 的价值不仅仅在于减少代码重复，更在于将领域逻辑从组件中剥离，让你的 UI 组件专注于它们的核心职责——UI 展示。
例如，与其在组件中堆砌如下的设置代码：

```tsx
useEffect(() => {
  const listener = () => setWidth(window.innerWidth);
  window.addEventListener('resize', listener);
  return () => window.removeEventListener('resize', listener);
}, []);
```

不如将其提取到一个 Hook 中：

```tsx
function useWindowWidth() {
  const [width, setWidth] = useState(
    typeof window !== 'undefined' ? window.innerWidth : 0
  );

  useEffect(() => {
    const listener = () => setWidth(window.innerWidth);
    window.addEventListener('resize', listener);
    return () => window.removeEventListener('change', listener);
  }, []);

  return width;
}
```
代码更整洁，更易于测试，且你的组件不再泄漏具体的实现细节。

👉🏻 SSR 技巧
始终提供一个确定性的回退值（fallback value）作为初始状态，以避免服务端渲染与客户端激活（Hydration）时不匹配的问题。

## 利用 useSyncExternalStore 管理订阅式状态

React 18 引入了 useSyncExternalStore，悄然解决了一大类与订阅、UI 撕裂（tearing）和高频更新相关的棘手 Bug。
如果你曾因 matchMedia、滚动位置或第三方状态库在不同渲染间表现不一致而苦恼，这正是 React 官方希望你使用的 API。

适用场景：
* 浏览器 API（matchMedia、页面可见性、滚动位置）
* 外部状态库（Redux、Zustand 或自定义订阅系统）
* 任何对性能敏感或事件驱动的数据源

```tsx
function useMediaQuery(query) {
  return useSyncExternalStore(
    (callback) => {
      const mql = window.matchMedia(query);
      mql.addEventListener('change', callback);
      return () => mql.removeEventListener('change', callback);
    },
    () => window.matchMedia(query).matches,
    () => false // SSR 回退值
  );
}
```
⚠️ 注意：useSyncExternalStore 会触发同步更新。它并非 useState 的直接替代品。

## 利用 Transitions 和 Deferred Values 打造丝滑 UI

当用户输入或筛选数据时，如果应用感觉卡顿，React 的并发工具（Concurrency Tools）可以派上用场。它们并非魔法，但能帮助 React 区分任务优先级：优先处理紧急更新（如输入），延后处理昂贵更新（如列表过滤）。

```tsx
const [searchTerm, setSearchTerm] = useState('');
const deferredSearchTerm = useDeferredValue(searchTerm);

const filtered = useMemo(() => {
  return data.filter(item => item.includes(deferredSearchTerm));
}, [data, deferredSearchTerm]);
```
这样，用户的打字体验保持流畅，而繁重的过滤计算则会被推迟执行。

简易心智模型：
* startTransition(() => setState()) → 推迟状态更新
* useDeferredValue(value) → 推迟派生值的计算

请按需配合使用，但切勿滥用。这些工具不适用于微不足道的计算。

## 编写可测试、可调试的 Hooks

现代 React DevTools 让检查自定义 Hooks 变得极其简单。如果你合理构建 Hooks，大部分逻辑甚至可以在不渲染实际组件的情况下进行测试。

* 将领域逻辑与 UI 分离
* 尽可能直接测试 Hooks
* 将 Provider 逻辑提取到独立的 Hook 中以提高清晰度

```tsx
function useAuthProvider() {
  const [user, setUser] = useState(null);
  const login = async (credentials) => { /* ... */ };
  const logout = () => { /* ... */ };
  return { user, login, logout };
}

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const value = useAuthProvider();
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
```
当你下次需要调试它时，你会感谢现在的自己。

## 超越 Hooks：迈向“数据优先”的 React 应用

React 正向着“数据优先”的渲染流演进，特别是随着服务端组件和基于 Action 模式的成熟。React 的目标并非 Solid.js 那样的细粒度响应式，而是更侧重于异步数据和服务器驱动的 UI。
值得关注的 API：
* use()：用于在渲染期间处理异步资源（主要用于服务端组件；通过 Server Actions 在客户端组件中提供有限支持）。
* useEffectEvent：用于创建稳定的 Effect 回调。
* useActionState：用于处理类似工作流的异步状态。
* 框架层面的缓存和数据原语。
* 更好的并发渲染工具和 DevTools。

方向很明确：React 希望我们减少对“瑞士军刀”般全能的 useEffect 的依赖，转而更多地拥抱清晰的、由渲染驱动的数据流。
围绕派生状态以及服务端/客户端边界来设计你的 Hooks，将使你的应用天然具备面向未来的能力。

## 总结：Hooks 是架构，而非单纯的语法
Hooks 不仅仅是比 Class 组件更优雅的 API，它们是一种架构模式。
1. 将派生状态保留在渲染逻辑中
2. 仅将 Effect 用于真正的副作用
3. 通过小而专注的 Hooks 组合逻辑
4. 利用并发工具平滑异步流程
5. 跨越客户端与服务端边界进行思考

React 在进化，我们的 Hooks 也应随之进化。
如果你还在用 2020 年的方式写 Hooks，这也没关系，大多数人都是如此。但 React 18+ 为我们提供了一个更强大的工具箱，尽早适应这些新模式，你将很快从中受益。
