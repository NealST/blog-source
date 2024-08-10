---
title: koa源码中的promise
date: 2018-11-12 14:34:43
tags: "node.js, koa"
---

koa 是一个非常轻量优雅的 node 应用开发框架，趁着双十一值班的空当阅读了下其源代码，其中一些比较有意思的地方整理成文与大家分享一下。

##  洋葱型中间件机制的实现原理

我们经常把 koa 中间件的执行机制类比于剥洋葱，这样设计其执行顺序的好处是我们不再需要手动去管理 request 和 response 的业务执行流程，且一个中间件对于 request 和 response 的不同逻辑能够放在同一个函数中，可以帮助我们极大的简化代码。在了解其实现原理之前，先来介绍一下 koa 的整体代码结构：

```
lib
|-- application.js
|-- context.js
|-- request.js
|-- response.js
```

application 是整个应用的入口，提供 koa constructor 以及实例方法属性的定义。context 封装了 koa ctx 对象的原型对象，同时提供了对 response 和 request 对象下  许多属性方法的代理访问，request.js 和 response.js 分别定义了 ctx request 和 response 属性的原型对象。

接下来让我们来看 application.js 中的一段代码：

```javascript
listen(...args) {
    debug('listen');
    const server = http.createServer(this.callback());
    return server.listen(...args);
}
callback() {
    const fn = compose(this.middleware);

    if (!this.listenerCount('error')) this.on('error', this.onerror);

    const handleRequest = (req, res) => {
      const ctx = this.createContext(req, res);
      return this.handleRequest(ctx, fn);
    };

    return handleRequest;
}
handleRequest(ctx, fnMiddleware) {
    const res = ctx.res;
    res.statusCode = 404;
    const onerror = err => ctx.onerror(err);
    const handleResponse = () => respond(ctx);
    onFinished(res, onerror);
    return fnMiddleware(ctx).then(handleResponse).catch(onerror);
}
```

上述代码展示了 koa 的基本原理，在其实例方法 listen 中对 http.createServer 进行了封装
，然后在回调函数中执行 koa 的中间件 ，在 callback 中，this.middleware 为业务定义的中间件函数所构成的数组，compose 为 koa-compose 模块提供的方法，它对中间件进行了整合，是构建 koa 洋葱型中间件模型的奥妙所在。从 handleRequest 方法中可以看出 compose 方法执行返回的是一个函数，且该函数的执行结果是一个 promise。接下来我们就来一探究竟，看看 koa-compose 是如何做到这些的，其  源代码和一段 koa 中间件应用示例代码如下所示：

```javascript
// compose源码
function compose (middleware) {
  if (!Array.isArray(middleware)) throw new TypeError('Middleware stack must be an array!')
  for (const fn of middleware) {
    if (typeof fn !== 'function') throw new TypeError('Middleware must be composed of functions!')
  }
  return function (context, next) {
    // last called middleware #
    let index = -1
    return dispatch(0)
    function dispatch (i) {
      if (i <= index) return Promise.reject(new Error('next() called multiple times'))
      index = i
      let fn = middleware[i]
      if (i === middleware.length) fn = next
      if (!fn) return Promise.resolve()
      try {
        return Promise.resolve(fn(context, dispatch.bind(null, i + 1)));
      } catch (err) {
        return Promise.reject(err)
      }
    }
  }
}

/*
** 中间件应用示例代码
*/
let Koa = require('koa')
let app = new Koa()
app.use(async function ware0 (ctx, next) {
  await setTimeout(function () {
    console.log('ware0 request')
  }, 0)
  next()
  console.log('ware0 response')
})
app.use(function ware1 (ctx, next) {
  console.log('ware1 request')
  next()
  console.log('ware1 response')
})
// 执行结果
ware0 request
ware1 request

ware1 response
ware0 response
```

从上述 compose 的源码可以看出，每个中间件所接受的 next 函数入参都是在 compose 返回函数中定义的 dispatch 函数，dispatch 接受下一个中间件在 middlewares 数组中的索引作为入参，该索引就像一个游标一样， 每当 next 函数执行后，游标向后移一位，以获取 middlaware 数组中的下一个中间件函数  进行执行，直到数组中最后一个中间件也就是使用 app.use 方法添加的最后一个中间件执行完毕之后再依次  回溯执行。整个流程实际上就是函数的调用栈，next 函数的执行就是下一个中间件的执行，只是 koa 在函数基础上加了一层 promise 封装以便在  中间件执行过程中能够  将捕获到的异常进行统一处理。 以上述编写的应用示例代码作为例子画出  函数执行调用栈示意图如下：  
![](https://i.loli.net/2018/11/12/5be9730b8c876.png)  
整个 compose 方法的实现非常简洁，核心代码仅仅 17 行而已，还是非常值得围观学习的。

## generator 函数类型中间件的执行

v1 版本的 koa 其中间件主流支持的是 generator 函数，在 v2 之后改而支持 async/await 模式，如果依旧使用 generator，koa 会给出一个 deprecated 提示，但是为了向后兼容，目前 generator 函数类型的中间件依然能够执行，koa 内部利用 koa-convert 模块对 generator 函数进行了一层包装，请看代码：

```
function convert (mw) {
  // mw为generator中间件
  if (typeof mw !== 'function') {
    throw new TypeError('middleware must be a function')
  }
  if (mw.constructor.name !== 'GeneratorFunction') {
    // assume it's Promise-based middleware
    return mw
  }
  const converted = function (ctx, next) {
    return co.call(ctx, mw.call(ctx, createGenerator(next)))
  }
  converted._name = mw._name || mw.name
  return converted
}

function * createGenerator (next) {
  return yield next()
}
```

从上面代码可以看出，koa-convert 在 generator 外部包裹了一个函数来提供与其他中间件一致的接口，内部利用 co 模块来执行 generator 函数，这里我想聊的就是 co 模块的原理，generator 函数  执行时并不会立即执行其内部逻辑，而是返回一个遍历器对象，然后通过调用该遍历器对象的 next 方法来执行，generator 函数本质来说是一个状态机，如果内部有多个 yield 表达式，就需要 next 方法执行多次才能完成函数体的执行，而 co 模块的能力就是实现 generator 函数的  自动执行，不需要手动多次调用 next 方法，那么它是如何做到的呢？co 源码如下：

```javascript
function co(gen) {
  var ctx = this;
  var args = slice.call(arguments, 1);

  // we wrap everything in a promise to avoid promise chaining,
  // which leads to memory leak errors.
  // see https://github.com/tj/co/issues/180
  return new Promise(function(resolve, reject) {
    if (typeof gen === "function") gen = gen.apply(ctx, args);
    if (!gen || typeof gen.next !== "function") return resolve(gen);

    onFulfilled();

    /**
     * @param {Mixed} res
     * @return {Promise}
     * @api private
     */

    function onFulfilled(res) {
      var ret;
      try {
        ret = gen.next(res);
      } catch (e) {
        return reject(e);
      }
      next(ret);
    }

    /**
     * @param {Error} err
     * @return {Promise}
     * @api private
     */

    function onRejected(err) {
      var ret;
      try {
        ret = gen.throw(err);
      } catch (e) {
        return reject(e);
      }
      next(ret);
    }

    /**
     * Get the next value in the generator,
     * return a promise.
     *
     * @param {Object} ret
     * @return {Promise}
     * @api private
     */

    function next(ret) {
      if (ret.done) return resolve(ret.value);
      // toPromise是一个函数，返回一个promise示例
      var value = toPromise.call(ctx, ret.value);
      if (value && isPromise(value)) return value.then(onFulfilled, onRejected);
      return onRejected(
        new TypeError(
          "You may only yield a function, promise, generator, array, or object, " +
            'but the following object was passed: "' +
            String(ret.value) +
            '"'
        )
      );
    }
  });
}
```

从 co 源码来看，它先是手动执行了一次 onFulfilled 函数来触发 generator 遍历器对象的 next 方法，然后利用 promise 的 onFulfilled 函数去自动完成剩余状态机的执行，在 onRejected 中利用遍历器对象的 throw 方法抛出执行上一次 yield 过程中遇到的异常，整个实现过程可以说是相当简洁优雅。

## 结语 

通过上面的例子  可以看出 promise 的能量是非常强大的，koa 的中间件实现和 co 模块的实现都是基于 promise，除了应用于日常的异步流程控制，在开发过程中我们还可以大大挖掘其潜力，帮助我们完成一些自动化程序工作流的事情。
