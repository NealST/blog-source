---
title: 聊聊 React-scan
date: 2024-12-18 21:11:10
tags:
  - React,Performance
---

## 前言

[react-scan](https://github.com/aidenybai/react-scan) 是 React 社区中最近热度很高的一个项目，在 github 上目前已经获得了 12.5k 的 star 量，主要用于自动检测 React 应用的性能问题(核心是组件的渲染性能)。针对该问题，之前社区中也有一些类似方案，但各自存在一些使用上的缺陷，比如：
* [React Profiler](https://react.dev/reference/react/Profiler)，React 官方提供的编码式性能检测方案，开发者可以在 onRender 函数中获取到应用渲染的性能数据，但缺陷是对应用源代码的侵入性较强，需要开发者额外处理生成环境的禁用，且开发者需要自行分析出可能的性能问题。
* [Why did you render](https://github.com/welldone-software/why-did-you-render), 其作者现已加入 React 团队，该工具通过检测应用的 re-render 原因来帮助开发者排查一些不必要的 re-render, 提供了工程化的接入方式，但缺陷是在性能可视化方面做的比较一般。
* [React Devtools](https://legacy.reactjs.org/blog/2018/09/10/introducing-the-react-profiler.html)，React 官方推出的一款开发者工具，可以通过其 profiler tab 来查看性能数据，但缺陷是缺少可编程的对外 API，无法做一些自定义的操作，同时也无法直观的看出哪些组件有问题。

相比上述方案，[react-scan](https://github.com/aidenybai/react-scan) 提供了更加低成本的接入方式，更为灵活的可编程 API 以及更高效的性能数据可视化方式，让开发者可以快速 get 到哪些组件需要进行性能优化。

## 安装使用

### 编程式接入

1. 安装依赖
```shell
npm i react-scan
```
2. 编码引入
```typescript
// 在 React 之前引入
import { scan } from 'react-scan';
import React from 'react';

if (typeof window !== 'undefined') {
  scan({
    enabled: true,
    // logs render info to console (default: false)
    log: true,
  });
}
```

### 命令行使用

```shell
npx react-scan@latest http://localhost:3000(your website url)
```

## 效果展示


## 实现原理

React-scan 的实现可分为两步，第一步是获取到 React 组件的渲染数据，第二步则是处理和分析数据，然后再通过一种高效的可视化和交互方式让开发者可以快速感知到 where the problem exists.

### 获取渲染数据

React 并未提供外部 API 可以获取组件的渲染或更新过程中的相关信息，因此，想要获取这部分数据，就必须能够切入到 React 执行的内部流程，React-scan 通过 [bippy](https://github.com/aidenybai/bippy) 这个库实现了这一点。而 bippy 的实现原理也并不复杂，它主要通过植入自定义的 `__REACT_DEVTOOLS_GLOBAL_HOOK__` 来获取到 React 执行过程中的相关信息。

具体来说，React-dom 在执行过程中会检测全局对象中是否存在 `__REACT_DEVTOOLS_GLOBAL_HOOK__` 这个对象，如果存在，React-dom 将会把该对象注入到内部钩子，概要代码如下：
```javascript
function injectInternals(internals) {
  if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ === 'undefined') {
    // No DevTools
    return false;
  }
  var hook = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  try {
    rendererID = hook.inject(internals); // We have successfully injected, so now it is safe to set up hooks.
    injectedHook = hook;
  } catch (err) {
    // ...
  } // DevTools exists
}
```
当 React 组件树在 commit 阶段执行渲染或更新 dom 时，React 会执行 内部的 onCommitRoot 生命周期方法，而该方法在运行时则会去检测并执行上述 hook 对象中的 onCommitFiberRoot 方法，概要代码如下：
```typescript
function onCommitRoot(root, priorityLevel) {
  if (injectedHook && typeof injectedHook.onCommitFiberRoot === 'function') {
    try {
      // ...
      injectedHook.onCommitFiberRoot(rendererID, root, priorityLevel, didError);
    } catch (err) {}
  }
}
```
所以，只要在植入的 `__REACT_DEVTOOLS_GLOBAL_HOOK__` 对象中实现自己的 onCommitFiberRoot 方法，即可拿到相关的渲染信息并执行一些自己的定制化逻辑。React-scan 就是这么干的，它在 onCommitFiberRoot 方法中进行了 fiber 树的递归遍历，并传入自定义的 handleRender 方法，每个需要更新的 fiberNode 在渲染时会执行该方法，概要代码如下所示：
```typescript
const onCommitFiberRoot = (rendererID: number, root: FiberRoot) => {
  if (instrumentation.isPaused.value) return;
  onCommitStart();
  if (root) {
    instrumentation.fiberRoots.add(root);
  }

  // 递归遍历 fiber 树
  traverseRenderedFibers(root, handleRender);

  onCommitFinish();
};
```
其中 handleRender 方法的实现如下所示（关键逻辑已添加注释）：
```typescript
const handleRender = (fiber: Fiber) => {
  const type = getType(fiber.type);
  if (!type) return null;
  if (!isValidFiber(fiber)) return null;
  
  // 计算 props 类型更新
  const propsRender = getPropsRender(fiber, type);
  // 计算 context 类型更新
  const contextRender = getContextRender(fiber, type);

  let trigger = false;

  // alternate 属性主要用于调和过程中链接到老的 fiberNode
  // 这里用于判断是否为 state 变化带来的 re-render
  if (fiber.alternate) {
    const didStateChange = traverseState(fiber, (prevState, nextState) => {
      return !Object.is(prevState.memoizedState, nextState.memoizedState);
    });
    if (didStateChange) {
      trigger = true;
    }
  }
  const name = getDisplayName(type);
  if (name === 'Million(Profiler)') return;
  
  const renders: Array<Render> = [];
  // props 变化引起的更新
  if (propsRender) {
    propsRender.trigger = trigger;
    renders.push(propsRender);
  }
  // context 变化引起的更新
  if (contextRender) {
    contextRender.trigger = trigger;
    renders.push(contextRender);
  }
  
  const { selfTime } = getTimings(fiber);
  // state 变化引起的更新
  if (trigger) {
    renders.push({
      type: 'state',
      count: 1,
      trigger,
      changes: [],
      name: getDisplayName(type),
      time: selfTime,
      forget: hasMemoCache(fiber),
    });
  }
  
  if (!propsRender && !contextRender && !trigger) {
    // 非 props,context 以及 state 变化带来的更新
    // 诸如通过调用 forceUpdate 带来的强制更新
    renders.push({
      type: 'misc',
      count: 1,
      trigger,
      changes: [],
      name: getDisplayName(type),
      time: selfTime,
      forget: hasMemoCache(fiber),
    });
  }
  
  // 展示渲染数据
  reportRender(fiber, renders);
};

```
通过上述代码可知，在 React 的 commit 阶段，在执行React-scan 自定义注入的 onCommitFiberRoot 方法时，React-scan 进行了 fiber 树的遍历，并在 handleRender 方法中通过比较 props, context 以及 state 等操作，算取了对应 fiberNode 的渲染数据，数据字段包括触发渲染的更新类型，渲染耗时等。

在 handleRender 中 React-scan 判断 props 和 context 更新以及执行相应的耗时计算实现如下：

```typescript
const getPropsRender = (fiber: Fiber, type: Function): Render | null => {
  const changes: Array<Change> = [];
  
  // alternate 属性可链接到老的 fiberNode
  const prevProps = fiber.alternate?.memoizedProps || {};
  const nextProps = fiber.memoizedProps || {};

  const props = new Set([
    ...Object.keys(prevProps),
    ...Object.keys(nextProps),
  ]);

  for (const propName in props) {
    const prevValue = prevProps?.[propName];
    const nextValue = nextProps?.[propName];

    if (
      Object.is(prevValue, nextValue) ||
      React.isValidElement(prevValue) ||
      React.isValidElement(nextValue)
    ) {
      continue;
    }
    const change: Change = {
      name: propName,
      prevValue,
      nextValue,
      unstable: false,
    };
    changes.push(change);

    const prevValueString = fastSerialize(prevValue);
    const nextValueString = fastSerialize(nextValue);

    if (
      !unstableTypes.includes(typeof prevValue) ||
      !unstableTypes.includes(typeof nextValue) ||
      prevValueString !== nextValueString
    ) {
      continue;
    }

    change.unstable = true;
  }

  return {
    type: 'props',
    count: 1,
    trigger: false,
    changes,
    name: getDisplayName(type),
    time: getTimings(fiber).selfTime,
    forget: hasMemoCache(fiber),
  };
};

export const getContextRender = (
  fiber: Fiber,
  type: Function,
): Render | null => {
  const changes: Array<Change> = [];

  const result = traverseContexts(fiber, (prevContext, nextContext) => {
    const prevValue = prevContext.memoizedValue;
    const nextValue = nextContext.memoizedValue;

    const change: Change = {
      name: '',
      prevValue,
      nextValue,
      unstable: false,
    };
    changes.push(change);

    const prevValueString = fastSerialize(prevValue);
    const nextValueString = fastSerialize(nextValue);

    if (
      unstableTypes.includes(typeof prevValue) &&
      unstableTypes.includes(typeof nextValue) &&
      prevValueString === nextValueString
    ) {
      change.unstable = true;
    }
  });

  if (!result) return null;

  const { selfTime } = getTimings(fiber);

  return {
    type: 'context',
    count: 1,
    trigger: false,
    changes,
    name: getDisplayName(type),
    time: selfTime,
    forget: hasMemoCache(fiber),
  };
};

export const getTimings = (
  fiber?: Fiber | null | undefined,
): { selfTime: number; totalTime: number } => {
  // fiberNode 的 actualDuration 属性表示该节点及其子节点在一次渲染中的实际渲染时间
  const totalTime = fiber?.actualDuration ?? 0;
  let selfTime = totalTime;
  
  let child = fiber?.child ?? null;
  // 减去子节点的耗时
  while (totalTime > 0 && child != null) {
    selfTime -= child.actualDuration ?? 0;
    child = child.sibling;
  }
  return { selfTime, totalTime };
};
```

至此，React-scan 解决问题的第一步-获取组件渲染数据这个难题就被解决了，下一步则是进行数据可视化，通过视觉处理让开发者能够高效的感知到组件渲染的性能问题。

### 可视化呈现数据



## 使用的注意事项

## 有了 React Compiler 之后还需要 React-scan 吗？

## 总结
