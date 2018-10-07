---
title: 彻底了解渲染引擎以及几点关于性能优化的建议
date: 2018-10-01 22:13:02
tags: "html, css, dom, engine"
---

在日常开发过程中，要编写性能足够优秀的代码，构造更加稳定的应用，我们不仅要对 javascript 本身的执行机制有深入的了解，更要对其宿主环境有更加深刻的认识，理解其工作原理以及组成结构，它可以帮助我们对 web 世界的运转模式有更高层级的认知。这次想要介绍的是浏览器的渲染引擎。

## 浏览器的构成

在具体介绍渲染引擎之前，我们先来看看浏览器的构成，看看渲染引擎在浏览器中扮演的是一个怎样的角色。关于浏览器的构成可以参见下图：

![](https://user-gold-cdn.xitu.io/2018/4/15/162c7da5b19bd249?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)  
如上图所示，浏览器从外到内的组成包括了以下几个部分：

1. User interface，即浏览器的视觉外观，具体包括其地址输入栏，前进后退键，书签菜单栏等等。
2. Browser engine, 浏览器引擎，它主要处理 User interface 与 render engine，即渲染引擎之间的交互。
3. Rendering engine, 即本文介绍的重点－渲染引擎，它负责解析 html 以及 css，并将解析后的内容渲染到屏幕上，完成 web 页面的展示。
4. Networking, 浏览器的网络处理层，主要负责处理 xhr 之类的网络请求，之后我也会专门写一篇文章来详细介绍它。
5. Javascript engine, 负责 javascript 的运行时处理，关于它我之前已经专门从内存管理和异步执行方面写了两篇文章，没有看过的可以参见我的其他文章哦。
6. Data persistence，数据持久化,即浏览器的本地数据存储，目前浏览器所支持的几种本地数据存储方式包括有 localstorage,indexDB,webSQL 以及 FileSystem。
   了解了渲染引擎在整个浏览器中的角色作用后，我们回到渲染引擎本身，看看它是如何完成页面渲染的。

##  渲染过程

渲染引擎接收到网络层传递过来的页面文档内容后，大致的解析处理过程如下：  
![](https://user-gold-cdn.xitu.io/2018/4/15/162c7fccbca93904?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### dom 树构造

首先解析 html 来构成 dom 树，假设有如下 html 文档内容：

```html
<html>
  <head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="theme.css">
  </head>
  <body>
    <p> Hello, <span> friend! </span> </p>
    <div>
      <img src="smiley.gif" alt="Smiley face" height="42" width="42">
    </div>
  </body>
</html>
```

解析后，其 dom 树构造示意图如下:  
![](https://user-gold-cdn.xitu.io/2018/4/15/162c802ddf2b8a56?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)  
可以看出 dom 树中每个节点的父子关系与 html 元素的父子关系保持一致。dom 树构造完成后还不能直接生成 render tree，还需要 cssom 树的配合。

### cssom 树

cssom 是指 css object model,当浏览器在解析 html 时如果在 head 中遇到了连接到外部 css 文件的 link 标签，浏览器就会立刻发起请求获取该 css 文件的内容，需要注意的是 css 文件的获取和解析不会阻塞 html 的解析,但是 script 标签的内容无论是下载还是执行都会阻塞 html 解析。假设页面中的 css 内容如下：

```css
body {
  font-size: 16px;
}

p {
  font-weight: bold;
}

span {
  color: red;
}

p span {
  display: none;
}

img {
  float: right;
}
```

浏览器会将其转换成如下的 cssom 树：  
![](https://user-gold-cdn.xitu.io/2018/4/15/162c8111e16c31a2?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)  
也许你会奇怪为什么 css 也会有这样的树形结构，这是因为浏览器在为某个 dom 对象计算最终的样式规则时，是先从最一般的规则开始，然后才是具体指定的规则。比如上述示例中，对于 span 标签，会先添加 body 中的 font-size 为 16px 的规则，然后才是它自己定义的规则，如果 span 标签包裹于某个 p 标签下还会添加 display 为 none 的规则，总结下来就是先 apply 父级规则，然后 apply specific rule.

### render 树

上述两项工作完成后，通过 dom 树与 cssom 树的结合就可以生成 render 树，或许你会问 render 树到底是什么？为什么一定要先生成 render 树，而不能直接用 dom 树和 cssdom 树去做 paint 呢？有这样的疑问很好，所谓 render 树，它其实是拥有样式表现的可见元素按照其文档顺序构造而成的树形结构，生成它的目的是确保元素的渲染过程是严格按照文档流顺序以及样式规则进行的。rener tree 的示意图如下：
![](https://user-gold-cdn.xitu.io/2018/4/15/162c83c63ff4bd29?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### layout

render 树虽然构造完成，但是其中的节点还需要进行位置和尺寸的计算，这些数值的计算过程就是 layout.
layout 是一个递归的过程，它从根元素也就是 html 元素开始计算，位置计算的坐标系也是相对于根元素，html 元素坐标为(0,0).后续的计算可能是局部更新也有可能是整体替换。
layout 过程结束后就意味着每个节点都会获得它将在屏幕上展示的位置坐标，可以开始进行真正的渲染过程了。

### painting

在这个阶段，浏览器就会把整个文档结构展示在页面上，与 layout 一样，painting 也有局部更新和全部更新两种可能。这取决于你的 dom 操作机制。
painting 是一个渐进的过程，为了更好的 UX 体验，渲染引擎不会等到所有 html 全部解析完成后才开始，而是先解析完成的部分先绘制，其余部分解析完成后再行绘制。
至此渲染引擎的整个执行流程已经结束，了解了渲染引擎的执行机制，下面我们就来看看可以从哪些方面入手去做页面的优化，以获得更好的用户体验。

## 关于性能优化

从渲染引擎的角度，我们可以从一下五个方面入手去做性能优化.

1. avascript, 在 js 代码编写过程中我们需要更多的注意会引起视觉变化的操作，比如 dom 操作等，尤其是在单页应用中，这样的场景更加常见。关于 javascript 方面的优化，我的建议是：

- 避免使用 setTimeout 或者 setInterval 这类定时器去操作视觉更新，因为它们的执行机制并不精准，有可能会离我们想要的时机相去甚远
- 将计算量大的操作交给 web workers,因为 js 的执行会阻塞页面的更新以及对用户交互的响应.
- 如果需要异步的操作 dom，那么请选择用 microtask 的方式，比如 mutationObserver。

2. css，在 css 编写过程中要尽量减少选择器的复杂度，相比给某个元素确定其样式规则，元素选择器的计算要多消耗 50%的时间。
3. ayout, 在 layout 过程中浏览器需要确定每个元素的坐标和尺寸，这意味着 layout 是一个计算密集型的过程，所以我们需要尽量减少重复触发 layout。针对 layout，我的优化建议是:

- 减少对元素位置和尺寸有影响的属性的操作，比如 width,height,left,top 等等，这些操作会使浏览器重新进行 layout.
- 尽可能使用 flexbox 进行布局，它比传统的基于盒模型的布局有更好的性能优势。
- 避免强制触发 layout,浏览器对于 dom 操作和属性的变化是有原生优化机制的，它会等到合适的时机将多个操作集中执行以避免高频触发 layout，但如果你在操作或更新了某个 dom 之后立即访问它的某些属性，比如 offsetHeight 这些，它就会立刻触发 layout,我们要尽量避免这样的访问。

## 总结

这篇文章主要介绍了浏览器渲染引擎的执行机制，相对来说是一篇非常偏基础知识的文章，也是我最近对前端基础重新梳理回顾对一次思考总结，希望也会对你有帮助。
