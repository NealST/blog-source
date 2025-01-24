---
title: 追求极致性能的框架 - Qwik
date: 2024-12-01 21:11:10
tags:
  - Framework,Front End
---

## Qwik 是什么

`Qwik` 是来源于社区的一个新的 `SSR` 前端研发框架，作者即为原 `angularJs` 框架的作者，其核心理念是页面启动时通过 `HTML` 直出和尽可能少的 `js` 实现秒开的页面体验以及无 `hydrate`（水合）过程以达到最快的页面可交互时间（TTI）。

## Qwik 核心想解决的问题是什么

在当前的 `web` 世界中，前端页面主要有两类技术实现 - `CSR` 和 `SSR`

* `CSR` 即客户端渲染，页面的渲染过程为先请求页面的诸多 js 资源，当 js 资源加载完成后开始执行，在执行过程中拉取服务端数据再依据这些数据完成页面渲染。主要的缺陷是页面白屏时间长，在互联网前期主要关注业务扩张的时候大量业务采用该方案。在当下业务进入存量竞争，性能体验成为主要矛盾的当下，大部分大厂已经逐步开始废弃该方案，转而纷纷接入 SSR 架构。
    
* `SSR` 即服务端渲染，页面的渲染过程为先在服务器上完成页面 `HTML` 的生成，然后返回给浏览器去渲染，但为了同步组件树的结构以及执行事件绑定让页面具备可交互能力，诸多前端框架比如 `React`，`Vue` 等，都会在浏览器端再全量执行一次 js，该过程称之为 `hydrate`。该方案的优点是用户能更快的看到页面内容，但是由于有 `hydrate` 过程的存在，会导致 `TTI` 时间拉长以及如果 `hydrate` 过程与服务器渲染生成的 `html` 结构不一致还会有额外的重排和重绘的性能损耗。

但无论是上述哪个渲染方式，都不可避免的是在页面初始化时会大量依赖 js 资源的加载和执行。随着业务持续迭代，加上站点所依赖使用的其他 js sdk，整个站点的 js bundle 量会非常庞大，而这会严重拖慢整个 web 页面，对于 js 资源的执行成本，可以看这篇文章[the cost of js（需翻墙）](https://medium.com/dev-channel/the-cost-of-javascript-84009f51e99e)。

此外，在 `SSR` 渲染架构下，为了减少页面可交互时间，提升页面的交互性，也需要解决 `hydrate` 的执行成本问题。

## Qwik 是如何解决的

`Qwik` 解决上述两个问题主要的策略是：

* 对 js 资源采用尽可能的懒加载和执行，页面启动时仅需小于 1kb 的初始化 js 资源。
    
* 在服务器端渲染完成后，将页面的渲染状态信息（包括组件树，事件绑定等）序列化到 `HTML dom` 中一并返回给浏览器端。这样在浏览器端就可以直接消费这些信息，而不需要像传统的 SSR 框架一样需要依赖整个应用的 JS 资源的下载和执行，这个特性在 `Qwik` 中称之为 `Resumable`.
    

### 关于懒加载

在当前的诸多前端框架中，对于资源的代码分割和懒加载处理是需要占用开发者大量心智负担的。以 `React` 为例：

```jsx
import { lazy, Suspense } from 'react';

const LazyComponent = lazy(() => import('../lazy-component'));

export default function Entry() {

  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        <LazyComponent />
      </Suspense>
    </div>
  )
  
}

```

但是在 `Qwik` 框架中，因为懒加载是其核心的设计哲学之一，`Qwik` 提供了自动化的编译器来让开发者不必感知具体的懒加载实现，只需要对需要进行懒加载的组件或事件实现进行标记即可，代码如下：

```jsx
// 通过 $ 符号来标识该组件是一个懒加载组件
export const Counter = component$(() => {
  const count = useSignal(0);
 
  // 通过 $ 符号来标识该事件实现需要懒加载和执行
  return <button onClick$={() => count.value++}>{count.value}</button>;
});
```

上述代码经过 Qwik optimizer 转换之后，会生成如下代码：

```jsx
const Counter = component(qrl('./chunk-a.js', 'Counter_onMount'));
```
```jsx
export const Counter_onMount = () => {
  const count = useSignal(0);
  return 
    <button onClick$={qrl('./chunk-b.js', 'Counter_onClick', [count])}> 
      {count.value}
    </button>;
};
```
```jsx
const Counter_onClick = () => {
  const [count] = useLexicalScope();
  return count.value++;
};
```

`Qwik` 框架的运行时会识别其编译器的产物，然后完成上述子 `chunk` 资源的加载和执行。除了上述示例中的组件和事件的懒加载，`Qwik` 还支持了副作用函数（effect）和样式资源的懒加载，可谓是万物皆可懒加载，大饼卷万物。

### 关于 Resumable

`Resumable` 的核心是 `Qwik` 会将服务器上的渲染信息序列化到 `Html dom` 中以方便端侧继续消费其渲染结果，从而避免 `hydrate` 的执行负担，极致化提升页面的响应性能，示意图如下：

![image](https://img.alicdn.com/imgextra/i1/O1CN01zbrdyK1xbBzq8YGZQ_!!6000000006461-0-tps-945-426.jpg)

`hydrate` 过程最重要的事情有两件，一是在 `dom` 元素上绑定事件使具备可交互的能力，二是在端侧建立组件树信息，并创建虚拟 dom, 这样当页面状态发生变化时才可以确定哪些组件需要 `re-render`。没有了 `hydrate` 过程之后，Qwik 是如何解决这两个关键问题的呢？

#### 事件绑定的处理

Qwik 在服务端渲染过程中会将元素的事件绑定序列化成固定的格式跟随 HTML 内容一起返回，以 button 元素的 click 事件为例，假设源码如下：

```jsx
// 通过 $ 符号来标识该组件是一个懒加载组件
export const Counter = component$(() => {
  const count = useSignal(0);
 
  // 通过 $ 符号来标识该事件实现需要懒加载和执行
  return 
    <button onClick$={() => console.log('hello, world')}>click me</button>;
});
```

经过序列化后，button 的 html 最终会变成如下的形式:

```jsx
<button on:click="./chunk.js#handler_symbol">click me</button>
```

Qwik 通过事件代理在页面全局安装了一个事件监听器，当上述点击事件触发时，该监听器会解析元素的 `on:click` 属性获取到对应的 chunk 资源和方法名称，然后加载该资源和执行其方法以响应用户的点击。这便解决了 hydrate 中的元素事件绑定问题。

#### 组件更新的实现

组件更新的本质是状态数据的响应，所以最主要的问题是建立状态与组件之间的绑定关系，当某个页面状态数据发生改变时对应消费了该状态数据的组件会重新渲染。Qwik 解决该问题的手段是 Proxy, 其执行流程如下：

* 在服务端完成页面的初始化渲染时，通过 proxy 数据对象的 get 方法来确定状态与组件的绑定关系，并将该绑定关系通过 `JSON.stringify` 的方式序列化到 HTML 中返回给端侧
    
* 当端侧响应某个事件更改某个状态数据时，在 `Proxy` 对象的 `set` 方法中读取该序列化数据获取到绑定关系，然后依次重新渲染相关组件
    
* 当组件重新渲染时，组件内的状态绑定关系会重新创建，下次更新状态数据时则会依据最新的绑定关系来判断是否要刷新组件。

可以看个具体的例子：

```jsx
export const ComplexCounter = component$(() => {
  // useStore 返回的是一个 proxy 对象
  const store = useStore({ count: 0, visible: true });
 
  return (
    <>
      <button onClick$={() => (store.visible = !store.visible)}>
        {store.visible ? 'hide' : 'show'}
      </button>
      <button onClick$={() => store.count++}>increment</button>
      {store.visible ? <p>{store.count}</p> : null}
    </>
  );
});
```

1. 初始化渲染时，`visible` 的值为 true
    
2. 当用户点击 `increment` 改变了 `count` 状态的值，由于最底部的 p 元素中读取了 count 字段，表示该组件绑定了 count, 此时 `ComplexCounter` 组件会重新渲染执行。
    
3. 当用户点击了 hide 后，组件再次重新渲染，最底部的 p 元素会消失，组件内不再存在对 count 字段的读取，组件状态绑定关系会重新更新。
    
4. 当用户再次点击 `increment` 改变 count 状态的值时，由于 count 字段的绑定关系不复存在，此时 `ComplexCounter` 组件不会重新渲染。
    
5. 当用户点击了 show 后，底部的 p 元素恢复存在，组件与 count 状态的绑定关系也会重新建立，当用户再次点击 `increment` 时会重新执行步骤 2
    

至此，Qwik 便解决了 `hydrate` 中的两个难题。但技术没有银弹，Qwik 也必定有其存在局限性的地方。

## Qwik 有哪些缺陷

首先，得于斯者毁于斯，因为使用了 `JSON.stringify` 来实现序列化，就必然会受限于 `JSON.stringify` 的限制，比如 `Date`, `Map`, `Set`, `URL` 等类型的对象就不支持。同时，流式数据的序列化也不支持。

其次，因为整个应用的运行大量依赖于服务端渲染数据的序列化，也会给开发者带来比较大心智负担，在开发过程中需要时刻关注序列化的内容和方式。

出于对其设计哲学的实现，`Qwik` 虽然形式上靠拢了 jsx 的编码方式，但是仍然是自定义了一套 dsl 和编译器，其组件生态并不能与社区的其他主流前端框架互通。

最后一点，由于做了极致了懒加载策略，当响应事件时就需要先去加载事件的 chunk 资源然后再去执行该资源中的某个方法，可能会因为网络等因素造成响应延迟或卡顿，同时 cdn 的访问压力也会增大。

## 对我们的启发

js 资源的加载和使用是有较大成本的，我们需要重新审视一下自己页面中的 js 资源加载状况。有一些没有用的 js 是不是可以逐步考虑做下线处理，以提升页面性能。同时，对于一些非重要组件或者非首屏可见的组件也可以考虑做更多的懒加载处理。

之前在 medium 上看到一篇文章 [a world without javascript](https://jonthanfielding.medium.com/the-web-unscripted-a-world-without-javascript-aa661a33e5a8), 也是非常有共鸣。
