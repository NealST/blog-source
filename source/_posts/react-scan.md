---
title: React-scan 是如何检测性能的
date: 2025-01-27 15:14:10
tags:
  - React,Performance
---

## 前言

[react-scan](https://github.com/aidenybai/react-scan) 是 React 社区中最近热度很高的一个项目，在 github 上目前已经获得了 12.5k 的 star 量，主要用于自动检测 React 应用的性能问题(核心是组件的渲染性能)。针对该问题，之前社区中也有一些类似方案，但各自存在一些使用上的缺陷，比如：
* [React Profiler](https://react.dev/reference/react/Profiler)，React 官方提供的编码式性能检测方案，开发者可以在 onRender 函数中获取到应用渲染的性能数据，但缺陷是对应用源代码的侵入性较强，需要开发者额外处理生成环境的禁用，且开发者需要自行分析出可能的性能问题。
* [Why did you render](https://github.com/welldone-software/why-did-you-render), 其作者现已加入 React 团队，该工具通过检测应用的 re-render 原因来帮助开发者排查一些不必要的 re-render, 提供了工程化的接入方式，但缺陷是在性能可视化方面做的比较一般。
* [React Devtools](https://legacy.reactjs.org/blog/2018/09/10/introducing-the-react-profiler.html)，React 官方推出的一款开发者工具(浏览器插件)，可以通过其 profiler tab 来查看性能数据，但缺陷是缺少可编程的对外 API，无法做一些自定义的操作，同时也无法直观的看出哪些组件有问题。

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

React 并未提供外部 API 可以获取组件的渲染或更新过程中的相关信息，因此，想要获取这部分数据，就必须能够切入到 React 内部的执行流程，React-scan 通过 [bippy](https://github.com/aidenybai/bippy) 这个库实现了这一点。而 bippy 的实现原理也并不复杂，它主要通过植入自定义的 `__REACT_DEVTOOLS_GLOBAL_HOOK__` 来获取到 React 执行过程中的相关信息。

具体来说，React-dom 在执行过程中会检测全局对象中是否存在 `__REACT_DEVTOOLS_GLOBAL_HOOK__` 这个对象，如果存在，React-dom 将会把该对象注入到内部钩子，概要代码如下：
```javascript
function injectInternals(internals) {
  if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ === 'undefined') {
    return false;
  }
  var hook = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  try {
    rendererID = hook.inject(internals); 
    injectedHook = hook;
  } catch (err) {}
}
```
React-scan 通过 [bippy](https://github.com/aidenybai/bippy) 植入 `__REACT_DEVTOOLS_GLOBAL_HOOK__` 的实现代码如下：
```typescript
try {
  // __REACT_DEVTOOLS_GLOBAL_HOOK__ 必须在 React 运行时之前植入
  if (isClientEnvironment()) {
    getRDTHook();
  }
} catch {}

export const getRDTHook = (
  onActive?: () => unknown,
): ReactDevToolsGlobalHook => {
  if (!hasRDTHook()) {
    // 植入自定义 hook
    return installRDTHook(onActive);
  }
  patchRDTHook(onActive);
  
  return globalThis.__REACT_DEVTOOLS_GLOBAL_HOOK__ as ReactDevToolsGlobalHook;
};

export const installRDTHook = (
  onActive?: () => unknown,
): ReactDevToolsGlobalHook => {
  const renderers = new Map<number, ReactRenderer>();
  let i = 0;
  const rdtHook: ReactDevToolsGlobalHook = {
    checkDCE,
    supportsFiber: true,
    supportsFlight: true,
    hasUnsupportedRendererAttached: false,
    renderers,
    onCommitFiberRoot: NO_OP,
    onCommitFiberUnmount: NO_OP,
    onPostCommitFiberRoot: NO_OP,
    inject(renderer) {
      const nextID = ++i;
      renderers.set(nextID, renderer);
      if (!rdtHook._instrumentationIsActive) {
        rdtHook._instrumentationIsActive = true;
        onActiveListeners.forEach((listener) => listener());
      }
      return nextID;
    },
    _instrumentationSource: BIPPY_INSTRUMENTATION_STRING,
    _instrumentationIsActive: false,
  };

  objectDefineProperty(globalThis, '__REACT_DEVTOOLS_GLOBAL_HOOK__', {
    value: rdtHook,
    configurable: true,
    writable: true,
  });
    
  return rdtHook;
};
```
当 React 组件树在 commit 阶段执行渲染或更新 dom 时，React 会执行内部的 `onCommitRoot` 生命周期方法，而该方法在运行时则会去检测并执行上述 hook 对象中的 `onCommitFiberRoot` 方法，概要代码如下：
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
所以，只要在植入的 `__REACT_DEVTOOLS_GLOBAL_HOOK__` 对象中实现自己的 `onCommitFiberRoot` 方法，即可拿到相关的渲染信息并执行一些自己的定制化逻辑。React-scan 就是这么干的，它在 `onCommitFiberRoot` 方法中进行了 fiber 树的递归遍历，并传入自定义的 `handleRender` 方法，每个需要更新的 fiberNode 在渲染时会执行该方法，概要代码如下所示：
```typescript
const onCommitFiberRoot = (rendererID: number, root: FiberRoot) => {
  if (instrumentation.isPaused.value) return;
  onCommitStart();
  if (root) {
    instrumentation.fiberRoots.add(root);
  }

  // 递归遍历 fiber 树,递归的逻辑这里不展开
  traverseRenderedFibers(root, handleRender);

  onCommitFinish();
};
```
其中 `handleRender` 方法的实现如下所示（关键逻辑已添加注释）：
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
通过上述代码可知，React-scan 在自定义注入的 `onCommitFiberRoot` 方法中进行了 fiber 树的遍历，并最终在 `handleRender` 方法内通过比较 props, context 以及 state 等操作，标记了多余的 re-render, 并算取了对应 fiberNode 的渲染数据，数据字段包括触发渲染的更新类型，渲染耗时等。

在 `handleRender` 中 React-scan 判断 props 和 context 更新以及执行相应的耗时计算实现如下：

```typescript

const unstableTypes = ['function', 'object'];

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
    // 如果是对象类型，则比较其序列化结果
    // 如果序列化结果比较值是相同，则说明其实该 re-render 是没必要的，通过 unstable 属性进行标记
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
      // 如果是对象类型，则比较其序列化结果
      // 如果序列化结果比较值是相同，则说明其实该 re-render 是没必要的，通过 unstable 属性进行标记
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
在上述代码中，React-scan 检测 props 和 context 更新时，通过 unstable 属性来标记了哪些更新是没必要的，在后续的可视化环节会重点绘制这些更新。

在接入方式上，React-scan 不仅支持通过 npm 包和 cdn script 的方式手动引入上述运行时代码，同时也支持通过命令行的方式来直接测试某个 URL 地址(参考安装使用环节的介绍)。在使用命令行时，React-scan 则通过 [playwright](https://playwright.dev/java/) 这个端到端测试开发框架提供的 API 来完成了 React-scan 运行时脚本的植入以及浏览器环境的控制与访问，核心概要代码如下：
```typescript
import {
  chromium,
  devices,
  type Browser,
  type BrowserContext,
} from 'playwright';

const init = async () => {
  intro(`${bgMagenta('[·]')} React Scan`);
  const args = mri(process.argv.slice(2));
  let browser: Browser | undefined;

  const device = devices[args.device];

  const contextOptions = {
    headless: false,
    channel,
    ...device,
    acceptDownloads: true,
    viewport: null,
    locale: 'en-US',
    timezoneId: 'America/New_York',
    args: [
      '--enable-webgl',
      '--use-gl=swiftshader',
      '--enable-accelerated-2d-canvas',
      '--disable-blink-features=AutomationControlled',
      '--disable-web-security',
    ],
    userAgent:
      userAgentStrings[Math.floor(Math.random() * userAgentStrings.length)],
    bypassCSP: true,
    ignoreHTTPSErrors: true,
  };

  browser = await chrome.launch({
    headless: false,
    channel: 'chrome'
  });

  const context = await browser.newContext(contextOptions);

  await context.addInitScript({
    content: `(() => {
      const NO_OP = () => {};
      let i = 0;
      globalThis.__REACT_DEVTOOLS_GLOBAL_HOOK__ = {
        checkDCE: NO_OP,
        supportsFiber: true,
        renderers: new Map(),
        onScheduleFiberRoot: NO_OP,
        onCommitFiberRoot: NO_OP,
        onCommitFiberUnmount: NO_OP,
        inject(renderer) {
          const nextID = ++i;
          this.renderers.set(nextID, renderer);
          return nextID;
        },
      };
    })();`,
  });

  const page = await context.newPage();
  
  /**
   * auto.global.js 的内容即为
   * import 'bippy';
     import { scan } from './index';

     if (typeof window !== 'undefined') {
       scan();
       window.reactScan = scan;
     }
   */
  const scriptContent = fs.readFileSync(
    path.resolve(__dirname, './auto.global.js'),
    'utf8',
  );

  const inputUrl = args._[0] || 'about:blank';

  await page.goto(inputUrl);
  
  const pollReport = async () => {
    if (page.url() !== currentURL) return;
    await page.evaluate(() => {
      const globalHook = globalThis.__REACT_SCAN__;
      if (!globalHook) return;
      const reportData = globalHook.ReactScanInternals.reportData;
      if (!Object.keys(reportData).length) return;
      let count = 0;
      for (const componentName in reportData) {
        count += reportData[componentName].count;
      }

      console.log('REACT_SCAN_REPORT', count);
    });
  };

  let count = 0;
  let currentSpinner: ReturnType<typeof spinner> | undefined;
  let currentURL = inputUrl;
  let interval:ReturnType<typeof setInterval>
  
  // 植入 React-scan 运行时
  const inject = async (url: string) => {
    if (interval) clearInterval(interval);
    currentURL = url;
    const truncatedURL = truncateString(url, 50);
    currentSpinner?.stop(`${truncatedURL}${count ? ` (×${count})` : ''}`);
    currentSpinner = spinner();
    currentSpinner.start(dim(`Scanning: ${truncatedURL}`));
    count = 0;

    try {
      await page.waitForLoadState('load');
      await page.waitForTimeout(500);

      const hasReactScan = await page.evaluate(() => {
        return Boolean(globalThis.__REACT_SCAN__);
      });

      if (!hasReactScan) {
        // 植入脚本
        await page.addScriptTag({
          content: scriptContent,
        });
      }

      await page.waitForTimeout(100);

      await page.evaluate(() => {
        if (typeof globalThis.reactScan !== 'function') return;
        globalThis.reactScan({ report: true });
        globalThis.__REACT_SCAN__.ReactScanInternals.reportData = {};
      });

      interval = setInterval(() => {
        // 轮询数据报告
        pollReport().catch(() => {});
      }, 1000);
    } catch (e) {
      currentSpinner?.stop(red(`Error: ${truncatedURL}`));
    }
  };

  await inject(inputUrl);
  
  // 检测跳转到新页面时，在新页面也植入 React-scan 脚本
  page.on('framenavigated', async (frame) => {
    if (frame !== page.mainFrame()) return;
    const url = frame.url();
    inject(url);
  });
  
  // 探测执行 console.log 时，打印出 React-scan 的检测数据
  page.on('console', async (msg) => {
    const text = msg.text();
    if (!text.startsWith('REACT_SCAN_REPORT')) {
      return;
    }
    const reportDataString = text.replace('REACT_SCAN_REPORT', '').trim();
    try {
      count = parseInt(reportDataString, 10);
    } catch {
      return;
    }

    const truncatedURL = truncateString(currentURL, 50);
    if (currentSpinner) {
      currentSpinner.message(
        dim(`Scanning: ${truncatedURL}${count ? ` (×${count})` : ''}`),
      );
    }
  });
};
```

至此，React-scan 完成了获取组件渲染数据这个关键的第一步，下一步则是进行数据可视化，通过视觉处理让开发者能够高效的感知到组件渲染的性能问题。

### 可视化呈现数据

从效果展示中可以看出 React-scan 会将组件每次更新的渲染信息通过边框（outline）的形式绘制在对应的 dom 元素上，以可视化的展示具体是哪个组件发生了更新以及具体的渲染次数和渲染耗时分别是多少。那么绘制的第一步便是先获取组件 fiberNode 所对应的 dom 元素及其矩形 box 信息。关键概要代码如下：

```typescript
const getOutline = (
  fiber: Fiber,
  render: Render,
): PendingOutline | null => {
  // 遍历组件下的 fiberNode 找到组件对应的根 dom 元素的 fiberNode
  const domFiber = getNearestHostFiber(fiber);
  if (!domFiber) return null;
  // 通过 fiberNode 的 stateNode 属性获取具体的 dom 元素
  const domNode = domFiber.stateNode;

  if (!(domNode instanceof HTMLElement)) return null;
  // 获取该 dom 元素的矩形 box 信息
  const rect = getRect(domNode);
  if (!rect) return null;

  return {
    rect,
    domNode,
    renders: [render],
  };
};

const getRect = (domNode: Element): DOMRect | null => {
  const now = performance.now();
  const cached = rectCache.get(domNode);
  // 避免重复计算或频繁计算
  if (cached && now - cached.timestamp < DEFAULT_THROTTLE_TIME) {
    return cached.rect;
  }

  const style = window.getComputedStyle(domNode);
  // 判断当前元素在页面中是否正常展示
  if (
    style.display === 'none' ||
    style.visibility === 'hidden' ||
    style.opacity === '0'
  ) {
    return null;
  }

  const rect = domNode.getBoundingClientRect();

  const isVisible =
    rect.bottom > 0 &&
    rect.right > 0 &&
    rect.top < window.innerHeight &&
    rect.left < window.innerWidth;

  if (!isVisible || !rect.width || !rect.height) {
    return null;
  }

  rectCache.set(domNode, { rect, timestamp: now });

  return rect;
};
```
完成第一步之后，React-scan 使用了 canvas 进行渲染信息的绘制，核心概要代码如下：
```typescript
const paintOutlines = async function (
  ctx: CanvasRenderingContext2D | OffscreenCanvasRenderingContext2D,
  outlines: Array<PendingOutline>,
): Promise<void> {
  return new Promise<void>((resolve) => {
    const activeOutlines = outlines.map((outline) => {
      const renders = outline.renders;
      const frame = 0;
      return {
        outline,
        alpha: 0.8,
        resolve,
        // 组装渲染次数与耗时的文案
        text: getLabelText(renders),
      };
    });

    requestAnimationFrame(() => {
      ctx.clearRect(0, 0, ctx.canvas.width / dpi, ctx.canvas.height / dpi);
      // 优先绘制栈顶数据
      for (let i = activeOutlines.length - 1; i >= 0; i--) {
        const activeOutline = activeOutlines[i];
        if (!activeOutline) continue;
        const { outline, text } = activeOutline;
        const { rect } = outline;
        const key = `${rect.x}-${rect.y}`;
        
        // 消费前面提过的 unstable 属性
        const isImportant = isOutlineUnstable(outline);
        // 通过透明度来重点标记不必要的 re-render
        const alphaScalar = isImportant ? 0.8 : 0.2;

        ctx.save();
        ctx.beginPath();
        // 根据对应 dom 元素的坐标和宽高绘制 dom 的边框矩形到 canvas 上
        ctx.rect(rect.x, rect.y, rect.width, rect.height);
        ctx.stroke();
        ctx.fill();

        ctx.restore();
        // 绘制对应 dom 渲染信息的文案, 渲染了多少次以及耗时多久
        if (text) {
          ctx.font = `11px Menlo,Consolas,Monaco,Liberation Mono,Lucida Console,monospace`;
          const textMetrics = ctx.measureText(text);
          const textWidth = textMetrics.width;
          const textHeight = 11;
          // 文案的横坐标与 dom 矩形一致
          const labelX: number = rect.x;
          // 文案的纵坐标放置在 dom 矩形上方
          const labelY: number = rect.y - textHeight - 4;
          
          // 绘制文本的矩形边框
          ctx.fillRect(labelX, labelY, textWidth + 4, textHeight + 4);

          ctx.fillStyle = `rgba(255,255,255,${alpha})`;
          // 绘制文本本身
          ctx.fillText(text, labelX + 2, labelY + textHeight);
        }
        ctx.restore();
      });
  });
}
```
该绘制所用的 canvas 为 React-scan 在初始化时创建，React-scan 创建了一个自定义元素，并且在创建过程中的处理非常严谨，为了防止横屏或者滚动时页面布局发生变化，也监听了相关事件并重新计算了 canvas 的宽高以及元素的 outline。核心代码如下：
```typescript
export const initReactScanOverlay = () => {
  class ReactScanOverlay extends HTMLElement {
    canvas: HTMLCanvasElement;
    // @ts-expect-error will be defined
    ctx: CanvasRenderingContext2D | OffscreenCanvasRenderingContext2D;

    constructor() {
      super();
      // 创建一个 shadow dom 来添加 canvas，避免影响外部文档结构
      const shadow = this.attachShadow({ mode: 'open' });
      this.canvas = document.createElement('canvas');
      this.setupCanvas();

      shadow.appendChild(this.canvas);
    }

    public getContext() {
      return this.ctx;
    }

    setupCanvas() {
      this.canvas.id = 'react-scan-canvas';
      this.canvas.style.position = 'fixed';
      this.canvas.style.top = '0';
      this.canvas.style.left = '0';
      this.canvas.style.width = '100vw';
      this.canvas.style.height = '100vh';
      this.canvas.style.pointerEvents = 'none';
      this.canvas.style.zIndex = '2147483646';
      this.canvas.setAttribute('aria-hidden', 'true');

      const isOffscreenCanvasSupported = 'OffscreenCanvas' in globalThis;
      const offscreenCanvas = isOffscreenCanvasSupported
        ? this.canvas.transferControlToOffscreen()
        : this.canvas;

      this.ctx = offscreenCanvas.getContext('2d') as
        | OffscreenCanvasRenderingContext2D
        | CanvasRenderingContext2D;

      let resizeScheduled = false;

      const resize = () => {
        const dpi = window.devicePixelRatio || 1;
        this.ctx.canvas.width = dpi * window.innerWidth;
        this.ctx.canvas.height = dpi * window.innerHeight;
        this.canvas.style.width = `${window.innerWidth}px`;
        this.canvas.style.height = `${window.innerHeight}px`;

        this.ctx.resetTransform();
        this.ctx.scale(dpi, dpi);

        resizeScheduled = false;
      };

      resize();
      
      // 页面 resize 或滚动时重新计算元素的 outline
      window.addEventListener('resize', () => {
        recalcOutlines();
        if (!resizeScheduled) {
          resizeScheduled = true;
          requestAnimationFrame(() => {
            resize();
          });
        }
      });
      window.addEventListener('scroll', () => {
        recalcOutlines();
      });
    }
  }
  // 创建一个自定义元素
  customElements.define('react-scan-overlay', ReactScanOverlay);

  return ReactScanOverlay;
};
```

至此，React-scan 也完成了渲染数据可视化的第二步，除了上述最核心的基础能力外，React-scan 也提供了一些额外的能力，包括可视化的工具栏来展示具体的渲染原因以及自定义监控和组件白名单过滤等能力，这里不再详细展开。

## 使用的注意事项

React-scan 项目本身并没有提到任何使用的注意事项，但其依赖的核心库 bippy 却是值得关注的，其 warning 如下：
![](https://img.alicdn.com/imgextra/i3/O1CN018BCSAi1MV6y9ZKlm3_!!6000000001439-0-tps-863-192.jpg)
解释一下，由于切入到了 React 内部的运行机制，bippy 可能会给应用造成一些预期之外的影响。同时，由于 React 内部运行机制可能会随着版本迭代有所变化，所以 bippy 也不能保证其能一直有效。换言之，其实并不建议在生产环境使用 React-scan, 可以在本地调试的过程中通过该工具来帮你发现和定位一些性能问题。

## 有了 React Compiler 之后还需要 React-scan 吗？

先说答案，当然是需要。React-compiler 解决的问题是让开发者不再需要去关注组件内的重复计算问题，不再需要手动通过 memo, useMemo 或 useCallback 来缓存组件和组件内的计算结果。可以说，有了 React compiler 以后，我们 React 应用的性能问题将会减少很多，但一些常见 case 仍无法避免，比如说像下面这种写法：
```tsx
<ExpensiveComponent onClick={() => alert('hi')} style={{ color: 'purple' }} />
```
由于 props 比较的是引用，对于 `ExpensiveComponent` 这个组件来说，每次其父组件 re-render 时，其 onClick 属性和 style 属性都会是一个新创建的对象，但其实对象内容并没有什么本质变化，此时，`ExpensiveComponent` 就会触发多余的 re-render，而 React-scan 则可以帮助我们去发现此类问题。

## 总结

从实现原理来说，React-scan 与 React Devtools 并没有什么本质的差别，都是通过植入自定义的 `__REACT_DEVTOOLS_GLOBAL_HOOK__` 对象来切入到 React 内部获取相关的渲染数据，然后进行数据可视化的呈现，但 React-scan 在技术产品化方面做的更好，它借鉴了一些已有工具的设计，与此同时，它在其基础上补足了相应的短板，在易用性（接入成本低），灵活性（提供可编程 api）以及问题排查效率（自动标记哪些是无必要更新）等方面均做了很多工作。此外，React-scan 的 roadmap 也显示出它是一个野心勃勃的项目，未来会支持更多性能类型的检测，比如页面加载，FPS 等，以及更多渲染类型的检测，比如 React Native.
