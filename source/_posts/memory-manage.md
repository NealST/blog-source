---
title: javascript的内存管理以及3种常见的内存泄漏
date: 2018-10-01 23:18:15
tags: "javascript, memory manage"
---

根据[GitHut stats](https://githut.info/)的统计数据显示，javascript 语言在 Github 中的活跃项目仓库数量和总的 push 数量已经登上了榜首的位置，而且在越来越多的领域里我们都能看 javascript 持续活跃的身影和不断前行的脚步  
![](https://user-gold-cdn.xitu.io/2017/12/10/1603e8b026b7739a?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

尽管我们正在越来越多的编写 Javascript 代码，但是我们不一定真的了解它。编写本系列专栏的目的就是深入到 javascript 的底层，了解其运行原理，帮助我们写出更高效的代码，减少一些不必要的 bug.
javascript 代码的执行分为 3 个部分：runtime, js engine, event loop，运行时(runtime)提供了 window，dom 等 API 注入，js 引擎负责内存管理，代码编译执行，事件循环则负责处理我们的异步逻辑，具体如下图所示：  
![](https://user-gold-cdn.xitu.io/2017/12/10/1603eac4434ce4c4?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)  
在这篇文章中我将主要探讨 javascript 内存管理，调用栈以及如何处理内存泄漏问题。 在后续的文章中我会继续介绍事件循环以及 js 引擎的执行机制。

## 内存管理

javascript 自带垃圾回收机制，它可以自动分配内存并回收不再使用的内存，这也使很多开发者认为我们没有必要去关注 js 的内存管理。但是我相信我们在平时开发过程中都或多或少的遇到过内存泄漏问题，理解 javascript 的内存管理机制可以帮助我们解决此类问题并写出更好的代码，而且作为一名程序员，我们也应当保持足够的好奇心去了解我们写出的代码在底层的运行原理。

### 内存是什么

在进入具体探讨之前，我们先来看下内存到底是什么。内存从物理意义上是指由一系列晶体管构成的可以存储数据的回路，从逻辑的角度我们可以将内存看作是一个巨大的可读写的比特数组。它存储着我们编写的代码以及我们在代码中定义的各类变量。对于很多静态类型编程语言来说，在代码进入编译阶段时编译器会根据变量声明时指定的类型提前申请分配给该变量的内存（比如，整型变量对应的是 4 个字节，浮点数对应 8 个字节）。内存区域分为栈空间和堆空间两部分，对于可以确定大小的变量，它们会被存储在栈空间中，比如：

```javascript
int n; // 4 bytes
int x[4]; // array of 4 elements, each 4 bytes
double m; // 8 bytes
```

还有一种类型的变量，不能在编译阶段就确定其需要多大的存储区域，其占用内存大小是在运行时确定的，比如:

```javascript
int n = readInput(); // n的大小依赖于用户的输入
```

对于这一类型的变量，它们会被存储在堆空间中。内存静态分配(static allocation)与动态分配(Dynamic allocation)的区别如下所示:  
![](https://user-gold-cdn.xitu.io/2017/12/10/1603f5e473ea9cc9?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### 内存生命周期

对于任何编程语言，内存的生命周期都基本一致，如下所示：  
![](https://user-gold-cdn.xitu.io/2017/12/10/1603f689c847ae60?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

1. 分配内存，在一些底层语言，比如 c 语言中我们也可以通过 malloc() 和 free()函数来手动完成内存的分配和释放。在 javascript 中这个过程是在我们做变量声明赋值时自动完成的，比如:

```javascript
var n = 374; // allocates memory for a number
var s = "sessionstack"; // allocates memory for a string
var o = {
  a: 1,
  b: null
}; // allocates memory for an object and its contained values
var a = [1, null, "str"]; // (like object) allocates memory for the
// array and its contained values
function f(a) {
  return a + 3;
} // allocates a function (which is a callable object)
// function expressions also allocate an object
someElement.addEventListener(
  "click",
  function() {
    someElement.style.backgroundColor = "blue";
  },
  false
);

// 函数调用触发的内存分配
var d = new Date(); // allocates a Date object
var e = document.createElement("div"); // allocates a DOM element

// 方法的调用也可以触发
var s1 = "sessionstack";
var s2 = s1.substr(0, 3); // s2 is a new string
// Since strings are immutable,
// JavaScript may decide to not allocate memory,
// but just store the [0, 3] range.
var a1 = ["str1", "str2"];
var a2 = ["str3", "str4"];
var a3 = a1.concat(a2);
// new array with 4 elements being
// the concatenation of a1 and a2 elements
```

2. 使用内存，变量完成内存分配之后我们的程序才可以使用它们，做一些读或写的操作。
3. 释放内存，当程序不需要再使用某些变量时，它们占用的内存就会进行释放，腾出空间。这里最大的问题是如何判定哪些变量是需要被回收的，对于像 javascript 这样的高级语言来说内存释放过程是由垃圾回收器完成的，它用于确定可回收内存的方法主要有两种：引用计数与标记清除。

#### 引用计数

在讨论该算法前，我们先来看下什么是引用（reference）。所谓引用是指一个对象与另一个对象的连接关系，如果对象 A 可以隐式或显式的访问对象 B，那么我们就可以说对象 A 拥有一个对对象 B 的引用，比如在 javascript 中一个 object 可以通过**proto**访问到其 prototype 对象（隐式），也可以直接访问其属性（显式）。

对于引用计数算法来说，它判定一个目标是可以被回收的标志就是该目标不再存在与其他对象的引用关系，比如：

```javascript
var o1 = {
  o2: {
    x: 1
  }
};
// 2 objects are created.
// 'o2' is referenced by 'o1' object as one of its properties.
// None can be garbage-collected

var o3 = o1; // the 'o3' variable is the second thing that
// has a reference to the object pointed by 'o1'.

o1 = 1; // now, the object that was originally in 'o1' has a
// single reference, embodied by the 'o3' variable

var o4 = o3.o2; // reference to 'o2' property of the object.
// This object has now 2 references: one as
// a property.
// The other as the 'o4' variable

o3 = "374"; // The object that was originally in 'o1' has now zero
// references to it.
// It can be garbage-collected.
// However, what was its 'o2' property is still
// referenced by the 'o4' variable, so it cannot be
// freed.

o4 = null; // what was the 'o2' property of the object originally in
// 'o1' has zero references to it.
// It can be garbage collected.
```

在上述示例中，o4 就是可以被回收的，引用计数在大多数情况下都是没什么问题的，但是当我们遇到循环引用它就会遇到麻烦，比如:

```javascript
function f() {
  var o1 = {};
  var o2 = {};
  o1.p = o2; // o1 references o2
  o2.p = o1; // o2 references o1. This creates a cycle.
}

f();
```

在上述示例中，o1,o2 互相引用，使得彼此都不能被释放。

#### 标记清除

标记清除判断某个对象是否可以被回收的标志是该对象不能再被访问到。其执行过程总共分为三步：

1. 确定根对象：在 javascript 中根对象主要是指全局对象，比如浏览器环境中的 window，node.js 中的 global。
2. 从根对象开始遍历子属性，并将这些属性变量标记为活跃类型，通过根对象不能访问到的就标记为可回收类型。
3. 根据第二步标记出来的结果进行内存回收。
   标记清除的算法执行示意图如下所示：  
   ![](https://user-gold-cdn.xitu.io/2017/12/10/160402af04313fa6?imageslim)

标记清除的算法比引用计数更优秀的地方在于它们对于可回收对象的判定方式上，一个对象不存在引用关系可以使该对象不能被访问到，而反过来则不一定成立，比如之前的循环引用问题，当函数执行完成之后，o1,o2 这两个变量都不能通过 window 查找到，在标记清除算法下会被当作可回收类型。
![](https://user-gold-cdn.xitu.io/2017/12/10/1604038b27722486?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### 内存泄漏

内存泄漏是指不再使用的内存区域没有被回收，导致这一块内存区域被白白浪费。虽然我们有前面提到的垃圾回收算法，但是我们在日常开发过程中仍然会时时遇到内存泄漏的问题，主要有以下三种类型：

1. 全局变量
   考虑以下这段代码：

```javascript
function foo(arg) {
  bar = "some text";
}
```

在这段代码中我们在函数 foo 里给变量 bar 赋值了一个字符串，但是我们没有在该函数作用域内先声明它，在 javascript 执行过程中，bar 会被挂载到全局变量 window 中(假设当前是浏览器环境)，当作是 window 的属性。这带来的问题是即使函数 foo 执行完毕，该变量仍然是可访问到的，其占用的内存不会得到释放，从而导致内存泄漏。
我们在日常开发过程中要尽量避免使用全局变量，除了污染全局作用域的问题，内存泄漏也是一个不容忽视的因素。

2. 闭包
   内部函数可以访问其外部作用域内的变量，闭包为我们编写 javascript 代码带来前所未有的灵活性，但是闭包也有可能会带来内存泄漏的风险。比如下面这段代码:

```javascript
var theThing = null;
var replaceThing = function() {
  var originalThing = theThing;
  var unused = function() {
    if (originalThing)
      // a reference to 'originalThing'
      console.log("hi");
  };
  theThing = {
    longStr: new Array(1000000).join("*"),
    someMethod: function() {
      console.log("message");
    }
  };
};
setInterval(replaceThing, 1000);
```

在函数 replaceThing 中，函数 unused 会形成一个闭包并含有对 originalThing 的引用，一旦 replaceThing 执行，theThing 会被赋予一个对象作为新值，在该对象中也会定义一个新的闭包 someMethod, 这两个闭包是在相同的父级作用域中创建的，因此它们会共享外部作用域。由于 someMethod 方法可以通过 theThing 在 replaceThing 外部访问到，即使 unused 没有被调用，它对变量 originalThing 的引用会使该作用域不会被回收。因为每个闭包作用域都含有对 longstr 的间接引用，这种状态下会导致大量的内存泄漏。

3. dom 引用，先来看下面这一段代码:

```javascript
var elements = {
  button: document.getElementById("button"),
  image: document.getElementById("image")
};
function doStuff() {
  elements.image.src = "http://example.com/image_name.png";
}
function removeImage() {
  // The image is a direct child of the body element.
  document.body.removeChild(document.getElementById("image"));
  // At this point, we still have a reference to #button in the
  //global elements object. In other words, the button element is
  //still in memory and cannot be collected by the GC.
}
```

在上述代码中我们在两个地方保存了对 image 元素的引用，当函数 removeImage 执行时尽管 image 元素被删除，但是全局变量 elements 中仍然存在对 button 元素的引用，内存回收时不会将该元素回收。
除此之外还有另一种情况也值得引起注意。如果你存在对某个 table cell(td 标签)的引用，当你在 dom 树中删除它所属的 table 但该引用并没有删除时也同样会发生内存泄漏，垃圾回收器并不会像你所想的那样回收所有只保留 cell，而是会将整个 table 都保存在内存中，因为该 table 是 cell 的父节点，该 cell 依然会保持对其父节点的引用。

### 调用栈(call stack)

调用栈是内存中的一块存储区域，它负责记录程序当前的执行位置，我们可以通过一个示例来看下调用栈的工作模式，先来看如下代码:

```javascript
function multiply(x, y) {
  return x * y;
}
function printSquare(x) {
  var s = multiply(x, x);
  console.log(s);
}
printSquare(5);
```

当这段代码开始执行时，调用栈会随着函数的调用发生变化  
![](https://user-gold-cdn.xitu.io/2017/11/22/15fe349fad9be420?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

当 printSquare 被调用时它会先进栈，在函数执行过程中调用了函数 multiply，函数 multiply 被压入栈顶，执行完成之后出栈。再来看另外一个示例:

```javascript
function foo() {
  throw new Error("SessionStack will help you resolve crashes :)");
}
function bar() {
  foo();
}
function start() {
  bar();
}
start();
```

当这段代码执行时报错提示如下所示:  
![](https://user-gold-cdn.xitu.io/2017/11/22/15fe34a06562522b?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

根据报错位置指示的函数名称，我们可以对整个调用栈的顺序一目了然。
调用栈的空间是有限的，当函数调用信息超过该空间大小，就会发生常见的堆栈溢出的错误，比如:

```javascript
function foo() {
  foo();
}
foo();
```

它会不断的调用自身，其调用栈存储示意图和执行报错如下所示:  
![](https://user-gold-cdn.xitu.io/2017/11/22/15fe34a06c23fb25?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

![](https://user-gold-cdn.xitu.io/2017/11/22/15fe34a0534c544f?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

## 结语

本篇文章主要探讨了 javascript 中的内存管理策略，介绍了内存的分配，内存的回收以及三种容易导致内存泄漏的场景还有代码执行用到的调用栈等等，属于 javascript 中比较基础但却容易忽视的知识点，希望对您有所帮助。
