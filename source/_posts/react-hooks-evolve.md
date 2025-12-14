---
title: 编写现代化 React Hooks 的最佳实践
date: 2025-12-14 18:34:58
tags: "React"
---

![](https://img.alicdn.com/imgextra/i3/O1CN014WaMLX1zbJQTNMQGP_!!6000000006732-2-tps-1024-1024.png)

## 前言

React Hooks 问世已有数年，但在日常很多场景和代码库中仍然充斥着最原始的那套写法：各种 useState 搭配沉重繁杂的 useEffect，以及各种无脑复制粘贴的代码。

**Hooks 的初衷不仅仅是生命周期方法的简单替代品，它本质上是一套设计系统，旨在构建更具表现力、更模块化的架构。**

随着 Concurrent React（即 React 18/19 版本推出的并发模式）的出现，React 的渲染机制也发生了很大变化，并带来了很多新的 API。本文结合一些实际示例和 React 官方所推崇的开发范式，整理了现代化 React Hooks 的最佳编写实践。

## useEffect 的滥用

useEffect 可能是最被滥用的 Hook，很多开发者会把它当瑞士军刀一样用来实现各种逻辑，比如获取数据、计算派生值，甚至是简单的状态切换等，组件会因此出现各种奇怪的行为，比如会在奇怪的时间点重新渲染，或者渲染次数远超预期等。

```typescript
useEffect(() => {
  fetchData();
}, [query]); 
// 如果 query 是一个引用类型，即使 query 的新值在逻辑上等同于旧值，这里也会重新运行
```

这种滥用主要是混淆了“派生状态”与“副作用”的使用，在 React 的推荐范式中，这两者的处理方式截然不同。

## 正确的 useEffect

React 的推荐用法是：
> 只在处理真正的副作用（即与外部世界交互）时使用 Effect。

其他所有逻辑，都应在渲染期间（Render Phase）通过派生计算完成。

```tsx
const filteredData = useMemo(() => {
  return data.filter(item => item.includes(query));
}, [data, query]);
```

在使用 useEffect 时，可以利用 useEffectEvent（React 19 中提供支持）来避免一些不必要的 effect 触发。

以一个典型的聊天室场景为🌰：
* 当 roomId 变化时，需要重新连接服务器
* 当服务器连接成功时，需要打印一条日志，日志中包含当前的 theme。

很多开发者可能会写出如下代码：
```javascript
function ChatRoom({ roomId, theme }) {
  useEffect(() => {
    const connection = createConnection(roomId);
    connection.connect();
    
    // 问题在这里：
    // 我们想访问 theme，就必须把它加到依赖数组里。
    // 结果：每次 theme 切换（比如由亮变暗），聊天室都会断开并重新连接！
    console.log(`Connected to ${roomId} with ${theme} theme`);
    
    return () => connection.disconnect();
  }, [roomId, theme]); // 依赖了 theme，导致不必要的重连
}
```
以上代码虽然也能实现，但每次 theme 值的变更都会导致 effect 的重复触发。这其实是不符合逻辑预期的，我们只是想在 effect 中拿到 theme 的最新值而已。而 useEffectEvent 就可以解决这个问题，它可以在 effect 内部访问最新的 props 或 state，搭配 useEffectEvent 的实现代码如下：

```javascript
function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    // 这里总是能拿到最新的 theme
    console.log(`Connected to ${roomId} with ${theme} theme`);
  });

  useEffect(() => {
    const connection = createConnection(roomId);
    connection.connect();
    
    // 2. 在 Effect 中调用它
    onConnected();
    
    return () => connection.disconnect();
  }, [roomId]); // ✅ 依赖数组只有 roomId！切换 theme 不会触发重连。
}
```
**当你需要在 effect 中获取到一些变量的最新值但又不想把这个变量加到 effect 依赖数组中使其可以触发 effect 执行时就非常适合引入 `useEffectEvent`**

在权衡是否使用 useEffect 时，建议的做法是确认这个行为是由外部因素（网络、DOM、订阅）驱动还是可以仅在渲染过程中计算出这个结果。如果是后者，使用 useMemo、useCallback 等 hook 即可，组件行为会更具可预测性。

>🙋🏻‍♂️ 提示
不要把 useEffectEvent 当作是规避依赖数组检查的“作弊码”。它是专门为了优化 Effect 内部的逻辑执行而设计。

## 自定义 Hooks：不止于复用，更在于封装

自定义 Hooks 的价值不仅仅在于减少代码重复，更在于将一些领域逻辑从组件中剥离，让你的 UI 组件专注于它们的核心职责 - UI 展示。
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
代码更整洁，更易于测试，且组件可以屏蔽具体的实现细节，更易于接入使用。

> 👉🏻 SSR 技巧
在设置初始状态时，始终提供一个确定性的回退值（fallback value），以避免服务端渲染与客户端水合（Hydration）时 dom 不匹配的问题。

## 使用 useSyncExternalStore 管理订阅式状态

React 18 引入了 useSyncExternalStore，悄然解决了一大类与订阅、UI 撕裂（在同一次渲染结果中，不同的组件对于相同数据源显示不同的值）和高频更新相关的棘手 Bug。

### 什么是 UI 撕裂
假设你有一个外部 Store（比如 state.count = 0），并且页面上有两个组件都依赖这个值：
* 组件 A（顶部）：显示 Count: 0
* 组件 B（底部）：显示 Count: 0

React 17（及以前）的处理方式：渲染是同步且不可中断的。一旦 React 开始渲染，它会一口气把组件 A 和组件 B 都计算完。在这个过程中，外部的 count 即使变了，React 也看不到（或者被阻塞了），所以 A 和 B 永远显示一样的值。

React 18（并发模式）的处理方式：渲染是可中断的。为了保持页面流畅，React 可能会先渲染组件 A，然后暂停一下去处理更紧急的任务（比如用户点击），然后再回来渲染组件 B。这就可能会出现如下问题：
1. 开始渲染：React 渲染 组件 A，读取 Store，拿到 count = 0。
2. 中断（Yield）：React 暂停渲染，把主线程让出来处理用户点击。
3. 外部更新发生：就在这个空档期，用户点击导致 Store 变成了 count = 1。
4. 恢复渲染：React 回来继续渲染 组件 B，再次读取 Store，拿到 count = 1。
5. 提交（Commit）：React 把结果画到屏幕上。

结果（UI 撕裂）：
* 用户看到顶部写着：Count: 0
* 用户看到底部写着：Count: 1

对于用户来说，界面处于一种“自相矛盾”的错误状态。

### 为什么高频更新会有问题
在处理高频数据（如 window.onresize、滚动位置）时如果我们用老办法（useEffect 监听变化 -> setState 更新），可能会出现如下问题：

1. 滞后：由于 React 18 可能会把 setState 视为低优先级更新（Transition），在你拖动窗口时，React 内部状态更新得可能会比浏览器慢，导致 UI 反应迟钝。

2. 闪烁：并发特性可能会导致视觉上的回退或闪烁。

### useSyncExternalStore 是如何解决的

`useSyncExternalStore` 的工作原理非常 tough。它告诉 React：

**“我正在读取一个外部数据源。这个数据源随时可能变。对于依赖这个数据的组件，请不要使用并发特性（不要中断渲染）。 如果你在渲染过程中发现这个数据变了，立刻作废当前渲染，强制重来。”**

它通过以下方式解决问题：
* 强制同步读取：在渲染期间（Render Phase），它会立即读取当前 Store 的值。
* 订阅变更：它会自动建立订阅。
* 防止撕裂：如果它检测到在渲染过程中 Store 的值发生了变化，它会触发同步更新（Synchronous Update），这本质上是退回到了 React 17 的行为，从而保证了数据的一致性。

`useSyncExternalStore` 适用于以下场景：
* 浏览器 API（matchMedia、页面可见性、滚动位置等信息）的状态订阅
* 外部状态（Redux、Zustand 或自定义订阅系统）的订阅
* 任何对性能敏感或事件驱动的数据源状态订阅

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

## 利用 Transitions 和 Deferred Values 打造丝滑 UI

当用户输入或筛选数据时，如果感觉卡顿，可以使用 Transitions 和 Deferred Values 等方法，它们并非银弹，主要用于告知 React 区分任务优先级：优先处理紧急更新（如输入），延后处理昂贵更新（如列表过滤）。

### 举个🌰

假设你有你有一个搜索框，下面展示 10,000 条数据。你每打一个字，React 都要做两件事：
1. 更新输入框：让 Input 里显示你刚刚打的字（比如从 "A" 变成 "AB"）。
2. 筛选列表：遍历 10,000 条数据，找出包含 "AB" 的项并渲染。

在 React 17及以前，这是一条单行道。React 会先把 10,000 条数据筛选完、渲染完，再把输入框里的字更新出来。结果就是你打字飞快，但屏幕上的字出不来，感觉键盘“粘手”或延迟，体验极差，这叫阻塞渲染（Blocking Rendering）。

React 18 引入了并发工具，允许把更新分为两类：
* 紧急更新 (Urgent updates)：
  - 例子：打字、点击、鼠标悬停。
  - 特点：必须立即响应，否则用户会有卡顿感
  - 待遇：优先执行。
* 过渡更新/昂贵更新 (Transition updates)：
  - 例子：根据搜索词筛选列表、渲染图表。
  - 特点：用户可以忍受微小的延迟（比如 100ms），甚至延迟还是符合用户心理预期的。
  - 待遇：可以被打断。

### Transitions 和 Deferred Values 是如何工作的？

#### startTransition
当使用 startTransition 时，本质是在告诉 React：“这个状态更新不急，你可以稍后处理。”

```javascript
// 紧急：立刻让输入框显示 value
setInputValue(e.target.value); 

startTransition(() => {
  // 不急：这个更新会导致列表重绘，可以慢一点
  setSearchQuery(e.target.value); 
});
```
效果：React 会先更新输入框，保证打字流畅。然后在后台悄悄计算列表。如果计算过程中用户又打了一个字，React 会放弃当前的计算，优先去处理新打的字。

#### useDeferredValue
当无法控制 State 的设置过程（比如值是从父组件作为 props 传下来的），可以用这个 Hook。

```javascript
// component 接收到了最新的 query，比如 "ABC"
const deferredQuery = useDeferredValue(query); 
// React 的逻辑：
// query 现在是 "ABC"（紧急，用于输入框回显）
// deferredQuery 暂时还是 "AB"（旧值，用于列表渲染）
// 等 CPU 空闲了，我再把 deferredQuery 变成 "ABC"
```
效果：输入框立刻变成了 "ABC"，但下方的列表可能在短时间内还显示 "AB" 的搜索结果，直到 React 处理完繁重的筛选任务。

这样，用户的打字体验保持流畅，而繁重的过滤计算则会被推迟执行。

简易心智模型：
* startTransition(() => setState()) → 推迟状态更新
* useDeferredValue(value) → 推迟派生值的计算

Transitions 和 Deferred Values 只是通过设置任务优先级来确保用户的体验流畅，但并不会真正带来性能上的提升，比如说如果筛选 10,000 条数据需要 500ms，用了这些方法，它依然需要 500ms（甚至略多一点点开销）。

## 编写可测试、可调试的 Hooks

现代 React DevTools 让调试自定义 Hooks 变得极其简单。如果你合理编写 Hooks，大部分逻辑甚至可以在不渲染实际组件的情况下进行测试，推荐的做法是：

* 将领域逻辑与 UI 分离
* 将 Provider 逻辑提取到独立的 Hook 中以提高可测试性

### 传统的大多数写法（逻辑耦合在组件中）
通常写 Context 时，我们习惯把所有逻辑直接写在 Provider 组件里：

```tsx
// AuthProvider.js
export function AuthProvider({ children }) {
  // 逻辑和 UI 混杂在一起
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    // 复杂的初始化逻辑...
  }, []);

  const login = async () => { ... }; // 复杂的登录逻辑

  // 最后返回 JSX
  return (
    <AuthContext.Provider value={{ user, login }}>
      {children}
    </AuthContext.Provider>
  );
}
```

这种写法的问题是：
* 测试成本高：想测试 login 函数就必须把 <AuthProvider> 渲染到虚拟 DOM 里，甚至还得在里面塞一个假组件来触发登录按钮，这种集成测试很重很费劲。
* 调试困难：在 React DevTools 中，你只能看到一个巨大的 AuthProvider，里面混杂了一堆 State 和 Effect，很难一眼看出哪个是核心逻辑。

### 更优雅的做法（逻辑与 UI 分离）

```tsx
// 这是一个纯逻辑 Hook，不涉及任何 JSX 渲染
// 我们可以叫它 "Engine" (引擎)
export function useAuthProvider() {
  const [user, setUser] = useState(null);

  const login = async (credentials) => { 
    const result = await api.login(credentials);
    setUser(result.user);
  };

  const logout = () => { setUser(null); };

  // 返回的是数据和方法，不是 JSX
  return { user, login, logout };
}

// 仅是一个 UI 包装器
export function AuthProvider({ children }) {
  // 1. 启动引擎
  const auth = useAuthProvider(); 
  
  // 2. 把引擎提供的返回通过 Context 传下去
  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
}
```

这样一来，测试会变得异常简单，由于 useAuthProvider 只是一个 Hook，可以直接用 `@testing-library/react-hooks` 对它进行单元测试，完全不需要渲染 AuthProvider 组件，也不需要 Context。测试代码示例(伪代码)：
```javascript
// 测试 useAuthProvider，完全不用管 Context 和组件
test('should login user successfully', async () => {
  // 直接运行 Hook
  const { result } = renderHook(() => useAuthProvider());

  // 此时 user 应该是 null
  expect(result.current.user).toBe(null);

  // 直接调用 login 方法
  await act(async () => {
    await result.current.login({ name: 'admin' });
  });

  // 此时 user 应该有值了
  expect(result.current.user).toEqual({ name: 'admin' });
});
```

同时，当你打开 React DevTools 插件时，你会清晰地看到一个名为 Hooks 的部分，里面有一个 `useAuthProvider`。
* `State: { user: ... }`
* 可以清楚地看到是这个 Hook 的状态在变，而不是那个巨大的组件在变。

## 总结

React 的演进方向正在从单纯的客户端视图库，向着 **数据优先（Data-First）** 的全栈架构迈进。

对比追求 Solid.js 那样的细粒度响应式，React 选择了另一条路：深耕异步数据流与服务器驱动 UI。随着 Server Components 的成熟以及 use()、useActionState 等新 API 的加入，官方意图非常明显：不要再把 useEffect 当瑞士军刀，而是拥抱更清晰的更职责分明的控制方式。

**Hooks 不止是语法，更是架构**

现代化的 Hooks 不再是简单的代码复用，而是一种架构模式。一个健壮且体验良好的现代 React 应用，应当遵循以下设计准则：
* 派生优先：能通过渲染逻辑计算得出的，不要引入新的 State 或 Effect。
* 边界清晰：仅将 Effect 用于真正的外部副作用，其余逻辑封装进小而美的自定义 Hook 中。
* 拥抱并发：利用 useDeferredValue 和 Transitions 平滑异步任务，区分轻重缓急。
* 全栈思维：不再局限于客户端，而是跨越 Client/Server 边界来设计数据流向。

React 在不断演进，Hooks 的编写也需要跟上节奏。

