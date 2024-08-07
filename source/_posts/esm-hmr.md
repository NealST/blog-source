---
title: 如何实现 esm 模块的热更新 HMR
date: 2020-08-20 22:30:10
tags: "javascript, Front-end engineering"
---

## 前言

最近在前端工程领域出现了一些新的工程化工具，诸如尤雨溪的 vite 以及已在 GitHub 社区斩获 8317 个 star 的 [snowpack](https://www.snowpack.dev/#what-is-snowpack%3F)，这些工具的优势除了内置支持 vue, react 等框架的运行和构建，很重要的一点是开发环境下应用的快速启动能力， snowpack 的启动耗时更是号称在 50ms 以内。笔者找了一个简单的 react 项目尝试了一下，证实其所言非虚。而之所以能达到这种效果，其原理在于它直接使用了 esm 模块来启动应用，相比 webpack 来说减少了模块打包构建生成 bundle 的耗时。  
目前主流浏览器均已支持在 script 中直接使用 esm 模块，但是本地开发中还需要解决 esm 模块热更新的问题，在模块代码变更时可以快速看到页面效果。接下来我会结合 snowpack 中的实现源码来讲解如何完成 esm 模块的热更新，首先来看一个用 react 编写的 demo。

## demo 展示

项目的主要目录结构和代码如下所示：
```
|--public
   |__index.html
|--src
   |__App.css
   |__App.jsx
   |__index.css
   |__index.jsx
   |__logo.svg
```  
App.css
![](https://img.alicdn.com/tfs/TB14lolIrj1gK0jSZFOXXc7GpXa-1126-1740.png)  

App.jsx
![](https://img.alicdn.com/tfs/TB13vgoIAT2gK0jSZFkXXcIQFXa-1294-1344.png)  

index.css
![](https://img.alicdn.com/tfs/TB14xSmkcKfxu4jSZPfXXb3dXXa-1666-840.png)

index.jsx
![](https://img.alicdn.com/tfs/TB13e7KX639YK4jSZPcXXXrUFXa-874-912.png)

通过 snowpack 启动后，本地构建信息如下所示：
![](https://img.alicdn.com/tfs/TB1RGkkIxD1gK0jSZFsXXbldVXa-553-166.png)   

页面效果如下图所示：
![](https://img.alicdn.com/tfs/TB1cKhRJkY2gK0jSZFgXXc5OFXa-780-1468.png)

## 原理分析

### 前端逻辑
在 Chrome 中打开该页面的调试面板，可以看到项目的页面结构以及静态资源，如下图所示：
![](https://img.alicdn.com/tfs/TB1sqkiIqL7gK0jSZFBXXXZZpXa-1024-932.png)   
![](https://img.alicdn.com/tfs/TB1aQ7pIuL2gK0jSZFmXXc7iXXa-1228-940.png)  

从上述示例图中可以看出 snowpack 直接使用了入口文件 index.jsx 的 esm 模块来启动应用。在 HTML 中要使用 esm 模块，只需要在 scrip 标签后添加 type="module" 即可，关于浏览器中 esm 模块的使用可以参考 v8 引擎下的这篇文章： https://v8.dev/features/modules#other-features 这里不做详细介绍。  

除了 __dist__/index.js 的入口文件， HTML 中还添加了 /liveload/hmr.js 的文件，而且 index.js 的入口文件中也注入了一些 import.meta.hot 的声明代码，此外， css 类型的文件也都变成了 css.proxy.js 的文件。接下来我们可以来看下 App.js 以及 index.css.proxy.js 的代码，看看是否也有同样的注入以及 css.proxy.js 都做了啥

App.js
![](https://img.alicdn.com/tfs/TB13dlYJfb2gK0jSZK9XXaEgFXa-2048-2280.png)

index.css.proxy.js
![](https://img.alicdn.com/tfs/TB11PacJkL0gK0jSZFtXXXQCXXa-2048-1164.png)  

从上述代码中可以看出在页面初始化时， snowpack 在模块原有代码基础之上还注入了一些用于模块热更新相关的代码，如下所示：
![](https://img.alicdn.com/tfs/TB1DAesJkT2gK0jSZFkXXcIQFXa-1530-588.png)
对于 css 模块来说， snowpack 将其转换为 js 进行管理， css 内容通过 js 添加 style 标签来处理。值得注意的是上述示例代码中的 import.meta.url 是 esm 模块内的一个全局变量，其取值为当前模块的资源路径。模块中被注入的热更新代码会使用资源路径 URL 将当前模块注册至客户端热更新管理中心，也就是页面 html 中添加的 liveload/hmr.js，该模块代码如下所示：
![](https://img.alicdn.com/tfs/TB1v17pkIKfxu4jSZPfXXb3dXXa-1548-5376.png)  

hmr.js 代码本身不算复杂，它的主要职责是管理页面上的 esm 模块，监听来自本地服务器的消息，然后根据消息类型来选择是刷新页面还是动态更新模块代码，可以用一张图来诠释 hmr.js 与其他模块之间的关系与运行时模块更新的逻辑：
![](https://img.alicdn.com/tfs/TB1M.OFJeH2gK0jSZFEXXcqMpXa-1079-747.png)  

每个模块通过调用 hmr.js 提供的 createHotContext 方法来注册模块，当本地服务器监听到本地代码的变更时会通过 websocket 向 hmr.js 发送消息告知哪个模块发生了改变， hmr.js 获取到需要更新的模块后，通过动态 import 的方式向本地服务器发送获取模块最新代码的请求，本地服务器收到请求后向前端推送代码，即可完成整体的热更新链路。

对于本地启动的服务器来说，它核心要做的包括三件事情：
* 页面启动时其各个模块资源的热更新代码注入
* 监听本地代码变更，然后发送消息给 hmr.js
* 响应客户端模块更新的请求，发送本地最新代码文件  

接下来通过这三点来拆解本地服务端的实现逻辑

### 本地服务端逻辑

#### 热更新代码注入的实现
本地服务器在发送代码文件至前端前通过 wrapResponse 方法对文件内容进行代码注入，如下所示：
![](https://img.alicdn.com/tfs/TB1nAl0eOcKOu4jSZKbXXc19XXa-1868-984.png)  

该方法内部由不同类型处理方法构成， wrapHtmlResponse 负责将 hmr.js 添加至 HTML 中。
![](https://img.alicdn.com/tfs/TB1xokQJeH2gK0jSZJnXXaT1FXa-1498-588.png)  

wrapEsmProxyResponse 负责处理类似之前 css.proxy.js 之类通过 js 来代理管理的模块，如下所示：
![](https://img.alicdn.com/tfs/TB1Vz.VJbj1gK0jSZFuXXcrHpXa-1682-1668.png)

wrapCssModuleResponse 主要处理 .module.css 类型的模块，其本质逻辑跟上述 wrapEsmProxyResponse 方法差异不大，也是转换成 js 来管理，这里就不贴代码了。来看最后一个
wrapJSModuleResponse 方法：
![](https://img.alicdn.com/tfs/TB1Aj3WJbj1gK0jSZFuXXcrHpXa-1632-804.png)  

以上方法就是本地服务端注入热更新代码的主要实现，逻辑都不复杂，简直可以说一目了然。  

#### 本地代码变更的监听和消息推送的实现

本地代码文件的监听 snowpack 采用了 [chokidar](https://www.npmjs.com/package/chokidar) 这个三方库来实现，这个库解决了 node.js 原生提供的 fs.watch 以及 fs.watchFile 等方法存在的一些弊端，比如：
* 不能递归监视文件树的问题
* 高 cpu 占用的问题
* 文件更新的事件经常会重复触发  
* 在 macos 上使用一些编辑器比如 sublime 修改代码时不会触发文件更新  

这里先不做深入探讨，有兴趣的读者可以自行搜索相关资料。在 webpack-dev-server 中用的也是该模块。实现文件监听的代码如下所示：
![](https://img.alicdn.com/tfs/TB1UMcRJbr1gK0jSZR0XXbP8XXa-1650-696.png)  

当文件更新触发 change 事件后，执行 onWatchEvent 方法将文件变更的消息推送到前端，代码逻辑如下图所示：
![](https://img.alicdn.com/tfs/TB1VeMZJoY1gK0jSZFCXXcwqXXa-1346-912.png)  
![](https://img.alicdn.com/tfs/TB1S5LjXc4z2K4jSZKPXXXAYpXa-1430-1056.png)

updateOrBubble 方法调用 hmrEngine 的 broadcastMessage 方法来播报更新事件，同时也会遍历该模块的 dependents 递归调用 updateOrBubble 方法进行 dependent 更新， hmrEngine 的代码如下所示：
![](https://img.alicdn.com/tfs/TB1RBA5Jbj1gK0jSZFOXXc7GpXa-1446-3792.png)  

在本地服务端，每个文件都通过 hmrEngine 的 entry 进行管理。 broadCastMessage 方法通过 websocket 发送 update 到前端。在接受到前端的模块更新请求
```
import(id + `?mtime=${updateID}`)
```
时，本地服务端需要响应该请求，发送模块最新代码。

#### 客户端模块更新请求响应的实现
本地服务器是通过 http.createServer 来启动的，模块请求响应以及文件发送的实现逻辑如下所示：
![](https://img.alicdn.com/tfs/TB1A074JXT7gK0jSZFpXXaTkpXa-2048-1308.png)  
![](https://img.alicdn.com/tfs/TB1X7U6JkL0gK0jSZFxXXXWHVXa-1582-660.png)  

到这里涉及模块热更新链路的逻辑就算完整了，本地服务端的实现其实也并不复杂，相信了解了原理之后你也可以实现一个热更新工具。

## 结语

本篇文章通过 snowpack 的源码介绍了 esm 模块热更新整体链路的实现原理。虽然直接使用 esm 模块可以加速应用启动，但是这也是在模块数量不多的情况下，如果模块数量超过 300 个，构建 bundle 的加载体验会比 esm 模块更好。

