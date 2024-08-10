---
title: 深入理解事件循环和异步流程控制
date: 2018-10-01 22:34:58
tags: "javascript, browser, async control"
---

javascript 的执行分为三个部分：运行时，事件循环，js 引擎。运行时提供了诸如注入全局 API（dom, setTimeout 之类）这样的功能。js 引擎负责代码编译执行，包括内存管理。之前写了一篇关于 javascript 内存管理的文章,具体可见 [javascript 内存管理以及三种常见的内存泄漏](https://nealst.github.io/2018/10/01/memory-manage/)
javascript 执行示意图如下所示:  
![](https://user-gold-cdn.xitu.io/2017/12/10/1603eac4434ce4c4?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)  
事件循环与回调队列相对应，负责处理我们的异步逻辑。本篇文章将会从事件循环的诞生背景(解决什么问题), 处理异步执行问题的思路(怎样解决的问题)以及 javascript 语言层面对于异步逻辑编写的封装

## 事件循环(event loop)

### 为什么我们需要事件循环

作为前端工程师，我们都知道 javascript 是单线程的。所谓单线程，就是在同一时间我们只能响应一个操作，这带来的问题是如果某个操作极为耗时，比如处理复杂的图像运算或者等待服务器返回数据的过程，典型的场景如下所示:

```javascript
// This is assuming that you're using jQuery
jQuery.ajax({
  url: "https://api.example.com/endpoint",
  success: function(response) {
    // This is your callback.
  },
  async: false // And this is a terrible idea
});
```

这个 ajax 请求以同步的方式进行调用，在接口返回数据之前 javascript 线程都会处于被占用的状态，会导致当前页面在 success 函数执行完成前不能响应用户的任何操作。如果这个过程持续时间过长，就会直接造成页面处于假死状态  
![](https://user-gold-cdn.xitu.io/2017/12/2/1601543248c01c17?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)  
如果有一种机制可以实现代码执行过程中无阻塞的响应用户操作，那么世界将更加美好。事件循环就是为此而生的，它的作用是监控调用栈和回调队列，调用栈负责处理 javascript 执行线程中的任务，遇到像 ajax 请求或者 setTimeout 这些异步逻辑时会执行它们，但不会阻塞后续任务的执行，当 ajax 请求或者定时器完成时其指定的回调会被放进回调队列中，等到调用栈空间没有正在执行的函数，事件循环就会从回调队列中提取回调函数压入调用栈执行。

### 事件循环的执行机制

让我们来看如下这段代码:

```javascript
console.log("Hi");
setTimeout(function cb1() {
  console.log("cb1");
}, 5000);
console.log("Bye");
```

执行这段代码，我们可以看下调用栈和任务队列中都发生了什么

1. 初始状态，调用栈和任务队列均空白  
   ![](https://user-gold-cdn.xitu.io/2017/12/2/1601543249419657?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

2. 添加 console.log('Hi')至调用栈  
   ![](https://user-gold-cdn.xitu.io/2017/12/2/160154324e9052b1?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

3. console.log('Hi')被执行  
   ![](https://user-gold-cdn.xitu.io/2017/12/2/16015432508aedd2?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

4. console.log('Hi')被移除出调用栈
   ![](https://user-gold-cdn.xitu.io/2017/12/2/160154330894b215?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

5. 添加 setTimeout(function cb1() { ... })至调用栈  
   ![](https://user-gold-cdn.xitu.io/2017/12/2/160154331199b438?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

6. setTimeout(function cb1() { ... })被执行，浏览器会根据 web API 创建一个定时器  
   ![](https://user-gold-cdn.xitu.io/2017/12/2/160154330e09555a?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

7. setTimeout(function cb1() { ... })执行完成并被移除出调用栈  
   ![](https://user-gold-cdn.xitu.io/2017/12/2/160154330a8d8b62?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

8. 添加 console.log('Bye')到调用栈  
   ![](https://user-gold-cdn.xitu.io/2017/12/2/1601543317ebdc27?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

9. 执行 console.log('Bye')  
   ![](https://user-gold-cdn.xitu.io/2017/12/2/160154331ec53e5a?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

10. console.log('Bye')被移除出调用栈，调用栈再度为空  
    ![](https://user-gold-cdn.xitu.io/2017/12/2/16015433d4609c45?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

11. 至少 5000ms 后，定时器执行完成，此时它会将 cb1 回调函数加入到回调队列中  
    ![](https://user-gold-cdn.xitu.io/2017/12/2/16015433c2729f6b?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

12. 事件循环检测到此时调用栈为空，将 cb1 取出压入到调用栈中  
    ![](https://user-gold-cdn.xitu.io/2017/12/2/16015433e131faca?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

13. cb1 被执行,console.log('cb1')被压入调用栈  
    ![](https://user-gold-cdn.xitu.io/2017/12/2/16015433db565749?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

14. console.log('cb1')被执行  
    ![](https://user-gold-cdn.xitu.io/2017/12/2/16015433f205eedd?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

15. console.log('cb1')被移除出调用栈  
    ![](https://user-gold-cdn.xitu.io/2017/12/2/16015433efd85463?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

16. cb1 被移除出调用栈  
    ![](https://user-gold-cdn.xitu.io/2017/12/2/1601543486371c57?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

整个流程的快速动画展示如下所示:

![](https://user-gold-cdn.xitu.io/2017/12/2/16015434824d2066?imageslim)  
通过上述示例的执行流程示意图我们可以很清楚的知道在代码执行过程中事件循环，调用栈，回调任务队列的合作机制。同时我们也可以注意到对于像 setTimeout 这一类的方法，其回调函数并不会像我们想象的那样是在我们指定的时刻执行，而是在该时刻它会被加入到回调队列中，等待调用栈没有在执行中的任务时才会由事件循环去读取它将其放到调用栈中执行，如果调用栈一直有任务在执行，那么该回调函数就会一直被阻塞，即使你传给 setTimeout 方法的时间参数为 0ms 也是一样。由此可见，异步任务的执行时机是不可预测的，可是我们要如何才能使不同的异步回调任务按照我们想要的顺序去执行呢，这就需要用到异步流程控制的解决方案了

## 异步流程控制

随着 javascript 语言的发展，针对异步流程控制也有了越来越多的解决方案，依照历史发展的车辙，主要有四种：

1. 回调函数  
   比如我们希望 xx2 的请求发生在 xx1 的请求完成之后，来看下面这段代码：

```javascript
// 以jquery中的请求为例
$.ajax({
  url: "xx1",
  success: function() {
    console.log("1");
    $.ajax({
      url: "xx2",
      success: function() {
        console.log("2");
      }
    });
  }
});
```

在上述代码中我们通过在 xx1 请求完成的回调函数中发起 xx2 的请求这种回调嵌套的方式来实现两个异步任务的执行顺序控制。这种回调函数的方式在 es6 出现之前是应用最为广泛的实现方案，但是其缺点也很明显，如果我们有多个异步任务需要依次执行，那么就会导致非常深的嵌套层次，造成回调地狱，降低代码可读性。

2. Promise  
   es6 中提供了 promise 的语法糖对异步流程控制做了更好的封装处理，它提供了更加优雅的方式管理异步任务的执行，可以让我们以一种接近于同步的方式来编写异步代码。还是以上述的两个请求处理作为示例:

```javascript
var ajax1 = function() {
  return new Promise(function(resolve, reject) {
    $.ajax({
      url: "xx1",
      success: function() {
        console.log("1");
        resolve();
      }
    });
  });
};
ajax1().then(() => {
  $.ajax({
    url: "xx1",
    success: function() {
      console.log("2");
    }
  });
});
```

promise 通过 then 方法的链式调用将需要按顺序执行的异步任务串起来，在代码可读性方面有很大提升。
究其实现原理，Promise 是一个构造函数，它有三个状态，分别是 pending, fullfilled,rejected，构造函数接受一个回调作为参数，在该回调函数中执行异步任务，然后通过 resolve 或者 reject 将 promise 的状态由 pending 置为 fullfilled 或者 rejected。
Promise 的原型对象上定义了 then 方法，该方法的作用是将传递给它的函数压入到 resolve 或者 reject 状态对应的任务数组中，当 promise 的状态发生改变时依次执行与状态相对应的数组中的回调函数，此外，promise 在其原型上还提供了 catch 方法来处理执行过程中遇到的异常。
Promise 函数本身也有两个属性 race,all。race,all 都接受一个 promise 实例数组作为参数，两者的区别在于前者只要数组中的某个 promise 任务率先执行完成就会直接调用回调数组中的函数，后者则需要等待全部 promise 任务执行完成。
一个 mini 的 promise 代码实现示例如下所示:

```javascript
function Promise(fn) {
  this.status = "pending";
  this.resolveCallbacks = [];
  this.rejectCallbacks = [];
  let _this = this;
  function resolve(data) {
    _this.status = "fullfilled";
    _this.resolveCallbacks.forEach(item => {
      if (typeof item === "function") {
        item.call(this, data);
      }
    });
  }
  function reject(error) {
    _this.status = "rejected";
    _this.rejectCallbacks.forEach(item => {
      if (typeof item === "function") {
        item.call(this, error);
      }
    });
  }
  fn.call(this, resolve, reject);
}
Promise.prototype.then = function(resolveCb, rejectCb) {
  this.resolveCallbacks.push(resolveCb);
  this.rejectCallbacks.push(rejectCb);
};
Promise.prototype.catch = function(rejectCb) {
  this.rejectCallbacks.push(rejectCb);
};
Promise.race = function(promiseArrays) {
  let cbs = [],
    theIndex;
  if (
    promiseArrays.some((item, index) => {
      return (theIndex = index && item.status === "fullfilled");
    })
  ) {
    cbs.forEach(item => {
      item.call(this, promiseArrays[theIndex]);
    });
  }
  return {
    then(fn) {
      cbs.push(fn);
      return this;
    }
  };
};
Promise.all = function(promiseArrays) {
  let cbs = [];
  if (
    promiseArrays.every(item => {
      return item.status === "fullfilled";
    })
  ) {
    cbs.forEach(item => {
      item.call(this);
    });
  }
  return {
    then(fn) {
      cbs.push(fn);
      return this;
    }
  };
};
```

以上是我对 promise 的一个非常简短的实现，主要是为了说明 promise 的封装运行原理，它对异步任务的管理是如何实现的。

3. Generator 函数  
   generator 也是 es6 中新增的一种语法糖，它是一种特殊的函数，可以被用来做异步流程管理。依旧以之前的 ajax 请求作为示例, 来看看用 generator 函数如何做到流程控制:

```javascript
function* ajaxManage() {
  yield $.ajax({
    url: "xx1",
    success: function() {
      console.log("1");
    }
  });
  yield $.ajax({
    url: "xx2",
    success: function() {
      console.log("2");
    }
  });
  return "ending";
}
var manage = ajaxManage();
manage.next();
manage.next();
manage.next(); // return {value: 'ending', done: true}
```

在上述示例中我们定义了 ajaxManage 这个 generator 函数，但是当我们调用该函数时他并没有真正的执行其内部逻辑，而是会返回一个迭代器对象，generator 函数的执行与普通函数不同，只有调用迭代器对象的 next 方法时才会去真正执行我们在函数体内编写的业务逻辑，且 next 方法的调用只会执行单个通过 yield 或 return 关键字所定义的状态，该方法的返回值是一个含有 value 以及 done 这两个属性的对象，value 属性值为当前状态值，done 属性值为 false 表示当前不是最终状态。
我们可以通过将异步任务定义为多个状态的方式，用 generator 函数的迭代器机制去管理这些异步任务的执行。这种方式虽然也是一种异步流程控制的解决方案，但是其缺陷在于我们需要手动管理 generator 函数的迭代器执行，如果我们需要控制的异步任务数量众多，那么我们就需要多次调用 next 方法，这显然也是一种不太好的开发体验。
为了解决这个问题，也有很多开发者写过一些 generator 函数的自动执行器，其中比较广为人知的就是著名程序员 TJ Holowaychuk 开发的[co 模块](https://github.com/tj/co)，有兴趣的同学可以多了解下。

4. async/await  
   async/await 是 es8 中引入的一种处理异步流程控制的方案，它是 generator 函数的语法糖，可以使异步操作更加简洁方便，还是用之前的示例来演示下 async/await 这种方式是如何使用的：

```javascript
async function ajaxManage() {
  await $.ajax({
    url: "xx1",
    success: function() {
      console.log("1");
    }
  });
  await $.ajax({
    url: "xx2",
    success: function() {
      console.log("2");
    }
  });
}
ajaxManage();
```

通过代码示例可以看出，async/await 在写法上与 generator 函数是极为相近的，仅仅只是将\*号替换为 async，将 yield 替换为 await，但是 async/await 相比 generator，它自带执行器，像普通函数那样调用即可。另一方面它更加语义化，可读性更高，它也已经得到大多数主流浏览器的支持
![](https://user-gold-cdn.xitu.io/2017/12/2/16015434c93e1b49?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)  
 async/await 相比 promise 可以在很多方面优化我们的代码，比如： - 代码更精简清晰，比如多个异步任务执行时，使用 promise 需要写很多的 then 调用，且每个 then 方法中都要用一个 function 包裹异步任务。而 async/await 就不会有这个烦恼。此外，在异常处理，异步条件判断方面，async/await 都可以节省很多代码。

```javascript
// `rp` is a request-promise function.
rp(‘https://api.example.com/endpoint1').then(function(data) {
 // …
});
// 使用await模式
var response = await rp(‘https://api.example.com/endpoint1');

// 错误处理
// promise的写法
function loadData() {
    try { // Catches synchronous errors.
        getJSON().then(function(response) {
            var parsed = JSON.parse(response);
            console.log(parsed);
        }).catch(function(e) { // Catches asynchronous errors
            console.log(e);
        });
    } catch(e) {
        console.log(e);
    }
}
// async/await处理
async function loadData() {
    try {
        var data = JSON.parse(await getJSON());
        console.log(data);
    } catch(e) {
        console.log(e);
    }
}
// 异步条件判断
// promise处理
function loadData() {
  return getJSON()
    .then(function(response) {
      if (response.needsAnotherRequest) {
        return makeAnotherRequest(response)
          .then(function(anotherResponse) {
            console.log(anotherResponse)
            return anotherResponse
          })
      } else {
        console.log(response)
        return response
      }
    })
}
// async/await改造
async function loadData() {
  var response = await getJSON();
  if (response.needsAnotherRequest) {
    var anotherResponse = await makeAnotherRequest(response);
    console.log(anotherResponse)
    return anotherResponse
  } else {
    console.log(response);
    return response;
  }
}
```

- 报错定位更加准确

```javascript
// promise
function loadData() {
  return callAPromise()
    .then(callback1)
    .then(callback2)
    .then(callback3)
    .then(() => {
      throw new Error("boom");
    });
}
loadData().catch(function(e) {
  console.log(err);
  // Error: boom at callAPromise.then.then.then.then (index.js:8:13)
});

// async/await
async function loadData() {
  await callAPromise1();
  await callAPromise2();
  await callAPromise3();
  await callAPromise4();
  await callAPromise5();
  throw new Error("boom");
}
loadData().catch(function(e) {
  console.log(err);
  // output
  // Error: boom at loadData (index.js:7:9)
});
```

- debug 调试问题
  如果你在 promise 中使用过断点调试你就会知道这是件多么痛苦的事，当你在 then 方法中设置了一个断点，然后 debug 执行时此时如果你想使用 step over 跳过这段代码，你会发现在 promise 中无法做到这点, 因为 debugger 只能跳过同步代码。而在 async/await 中就不会有这个问题，await 的调用可以像同步逻辑那样被跳过。

## 结语

事件循环是宿主环境处理 javascript 单线程带来的执行阻塞问题的解决方案，所谓异步，就是当事件发生时将指定的回调加入到任务队列中，等待调用栈空闲时由事件循环将其取出压入到调用栈中执行，从而达到不阻塞主线程的目的。因为异步回调的执行时机是不可预测的，所以我们需要一种解决方案可以帮助我们实现异步执行流程控制，本篇文章也针对这一问题分析了当前处理异步流程控制的几种方案的优缺点和实现原理。希望能对大家有所帮助。
