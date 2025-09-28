---
title: Bun install 如何做到极致的包安装速度
date: 2025-09-27 18:10:00
tags: "Front-end engineering"
---

## 前言

`Bun install` 命令安装依赖包的速度堪称极致，平均而言，它比 npm 快 7 倍，比 pnpm 快 4 倍，比 yarn 快 17 倍。这种速度优势在依赖众多的大型前端工程中会体现的非常明显，其安装耗时直接从分钟级干到毫秒级。

它能达到这个效果的核心原因在于它针对安装过程中的每个环节都做了极致性的设计和实现，包括优化系统调用，消除 javascript 开销，异步 dns 解析，二进制 Manifest 缓存，优化 tarball 提取，利于缓存的数据结构设计，锁文件格式的优化，文件复制过程的优化以及多核利用的并行化处理等，令人叹为观止，感受到了其做底层基建的匠心。

废话不多说，直接看具体的手段实现。

## 优化系统调用

### 什么是系统调用

软件程序无法直接与计算机的硬盘，网络等打交道，我们的代码每次在执行一些操作（诸如文件读写，网络连接，分配内存）时都需要经过操作系统的调用来实现，这称之为系统调用。

### 为什么需要优化系统调用

计算机的 CPU 可以在两种模式下运行程序，一种是用户模式，一种是内核模式。

我们的应用代码主要在用户模式下运行，这种模式下的程序无法直接访问计算机的硬件，物理内存，这种设计的目的主要是防止程序相互干扰致使系统崩溃。

内核模式则主要是应用于操作系统内核的运行，用于管理资源，例如调度进程以使用 CPU、处理内存以及磁盘或网络设备等硬件。只有内核和设备驱动程序在该模式下运行！

所以当我们的代码在执行系统调用时，CPU 会进行模式切换，在模式切换时，CPU 会经历停止执行程序 → 保存其所有状态 → 切换到内核模式 → 执行操作 → 然后切换回用户模式的过程。这个模式切换的成本是比较高的，单词切换就需要耗费 1000-1500 个 CPU 周期。在 3GHz 处理器上，1000-1500 个周期大约是 500 纳秒。这听起来可以忽略不计，但现代 SSD 每秒可以处理超过 100 万次作。如果每个作都需要系统调用，那么仅在模式切换时，就需要 15 亿个周期。

依赖包安装的过程会进行数千次系统调用。像React 这种库及其依赖项甚至可能会触发 50,000+ 次系统调用，意味着仅模式切换就损失了几秒钟的 CPU 时间！这还不包括读取文件或安装软件包的耗时。

### Bun 是怎么优化的


## 消除 javascript 开销

npm, pnpm, yarn 均采用 Node.js 编写，在 Node.js 中调用 fs.readFile 时，会经过一个复杂的管道，包括：
1. JavaScript 验证参数并将字符串从 UTF-16 转换为 UTF-8，以适配于 libuv 的 C API。这会在任何 I/O 启动之前短暂地阻塞主线程。
2. libuv 将该处理请求加入到 4 个工作线程的处理队列中。如果所有线程都无空闲，则请求将持续等待。
3. 工作线程拾取请求，打开文件描述符，并进行实际的 `read()` 系统调用。
4. CPU 切换到内核模式，从磁盘获取数据，并将其返回到工作线程。
5. 工作线程通过事件循环将文件数据推送回主线程，最终规划和执行你的回调。

每个 `fs.readFile()` 调用都会经过此管道。包安装过程会涉及数千个 package.json 文件的读取：扫描目录、处理依赖项元数据等。每次线程调度时（例如，在访问任务队列或向事件循环发出信号时），可以使用 futex 系统调用（Fast Userspace Mutex, Linux 内核提供的一种基础同步机制，用于实现高效的锁和同步原语。它结合了用户空间操作的快速性和内核空间阻塞的可靠性，是现代多线程编程的核心组件）来管理锁或等待。

数千次这种复杂的管道执行带来的系统调用开销相当高昂。而 Bun 是用 Zig 语言（对标 rust 的另一种系统编程语言）编写的，可编译为具有直接系统调用访问权限的本机代码。

```zig
// Direct system call, no JavaScript overhead
var file = bun.sys.File.from(try bun.sys.openatA(
    bun.FD.cwd(),
    abs,
    bun.O.RDONLY,
    0,
).unwrap());
```

当 Bun 读取文件时，Zig 代码直接进行系统调用，内核立即执行系统调用并返回数据，中间没有任何 javascript 引擎解析，线程池，事件循环等处理流程，性能差异不言而喻。

| Runtime | Version | Files/Second | Performance |
| --- | --- | --- | --- |
| **Bun** | v1.2.20 | **146,057** |  |
| Node.js | v24.5.0 | 66,576 | 2.2x slower |
| Node.js | v22.18.0 | 64,631 | 2.3x slower |

在此基准测试中，Bun 每秒处理 146,057 个 package.json 文件，而 Node.js v24.5.0 处理 66,576 个，v22.18.0 处理 64,631 个，快了 2 倍多！

Bun 基本没有任何运行时负担，每个文件的 0.019 毫秒就代表了其实际的 I/O 开销。而基于 Node.js 编写的包管理器由于 Node.js 本身的运行时解析成本和底层抽象成本，相同的读文件操作就需要耗费 0.065 毫秒。


## 异步 DNS 解析

安装依赖意味着需要处理网络请求，从 registry 上拉取依赖包信息，这就需要获取 registry.npmjs.org 等域名的 IP 地址。

对基于 Node.js 编写的包管理器来说，执行 dns 解析主要通过 `dns.lookup()` 方法来实现，这个方法看似异步，实则其内部实现为 `getaddrinfo()` 方法的调用，在 libuv 的线程池上运行时仍然会阻塞该子线程。

在 macOS 系统上 Bun 采用了 Apple 提供的一个隐藏异步 dns 查询 API - `getaddrinfo_async_start()`, 这个 API 不在 POSIX 标准之中，它允许 Bun 使用 mach 端口（Apple 的进程间通信方式）实现完全异步运行的 dns 解析请求。

## 二进制 Manifest 缓存

在正式安装依赖包之前，包管理器会先下载依赖包的 manifest 文件(内容包括这个包的版本记录，依赖项和元数据等)，对于一些像 React 这种具有 100+ 版本的流行包，其 manifest 文件大小可能会达到几兆大小。以 lodash 为例，其 manifest json 文件内容如下所示：
```json
{
  "name": "lodash",
  "versions": {
    "4.17.20": {
      "name": "lodash",
      "version": "4.17.20",
      "description": "Lodash modular utilities.",
      "license": "MIT",
      "repository": {
        "type": "git",
        "url": "git+https://github.com/lodash/lodash.git"
      },
      "homepage": "https://lodash.com/"
    },
    "4.17.21": {
      "name": "lodash",
      "version": "4.17.21",
      "description": "Lodash modular utilities.",
      "license": "MIT",
      "repository": {
        "type": "git",
        "url": "git+https://github.com/lodash/lodash.git"
      },
      "homepage": "https://lodash.com/"
    }
    // ... 100+ more versions, nearly identical
  }
}
```
对于包管理器来说，这种 manifest 描述文件的问题在于每次安装依赖包时，即使通过缓存的手段避免了文件的再次加载，但依然需要解析该 json 文件，除了语法验证，ast 构建，gc 管理等解析本身的开销以外，还有大量的内存冗余消耗问题。以上述的 lodash 为例，字符串 `Lodash modular utilitie`， `https://lodash.com/`，`git+https://github.com/lodash/lodash.git` 重复出现在每个版本中。在 json 解析时，js 会在内存中为每个字符串都创建一个单独的字符串对象，这就导致了有很多重复的内存浪费。

Bun 解决这个问题的方式为通过二进制格式来存储 manifest 描述。当下载 manifest 文件时，它会解析一次 JSON 将其存储为二进制文件（~/.bun/install/cache/ 中的 .npm 文件），并将所有包信息（版本、依赖项、校验和等）存储于特定的字节偏移量中。

当 Bun 访问名称 `Lodash modular utilitie` 时，它只是进行指针的算数运算：`string_buffer + offset`，没有解析，对象遍历和内存分配。
```
// Pseudocode

// String buffer (all strings stored once)
string_buffer = "lodash\0MIT\0Lodash modular utilities.\0git+https://github.com/lodash/lodash.git\0https://lodash.com/\04.17.20\04.17.21\0..."
                 ^0     ^7   ^11                        ^37                                      ^79                   ^99      ^107

// Version entries (fixed-size structs)
versions = [
  { name_offset: 0, name_len: 6, version_offset: 99, version_len: 7, desc_offset: 11, desc_len: 26, license_offset: 7, license_len: 3, ... },  // 4.17.20
  { name_offset: 0, name_len: 6, version_offset: 107, version_len: 7, desc_offset: 11, desc_len: 26, license_offset: 7, license_len: 3, ... }, // 4.17.21
  // ... 100+ more version structs
]
```

benchmark 测试下显示即使是缓存下的 `npm install` 也比无缓存的 Bun 安装要慢。
```
Benchmark 1: bun install # fresh
  Time (mean ± σ):     230.2 ms ± 685.5 ms    [User: 145.1 ms, System: 161.9 ms]
  Range (min … max):     9.0 ms … 2181.0 ms    10 runs

Benchmark 2: bun install # cached
  Time (mean ± σ):       9.1 ms ±   0.3 ms    [User: 8.5 ms, System: 5.9 ms]
  Range (min … max):     8.7 ms …  11.5 ms    10 runs

Benchmark 3: npm install # fresh
  Time (mean ± σ):      1.786 s ±  4.407 s    [User: 0.975 s, System: 0.484 s]
  Range (min … max):    0.348 s … 14.328 s    10 runs

Benchmark 4: npm install # cached
  Time (mean ± σ):     363.1 ms ±  21.6 ms    [User: 276.3 ms, System: 63.0 ms]
  Range (min … max):   344.7 ms … 412.0 ms    10 runs

Summary
  bun install # cached ran
    25.30 ± 75.33 times faster than bun install # fresh
    39.90 ± 2.37 times faster than npm install # cached
   	196.26 ± 484.29 times faster than npm install # fresh
```

## Tarball 提取

在处理完 manifest 描述文件后，包管理器会从 registry 上下载并提取 tarball 文件（即压缩的存档文件，如 .zip 文件，其中包含每个包的实际源代码和文件）。

大多数包管理器通过流式传输来接收 tarball 文件数据，并在接收到数据时进行解压缩，整个过程从一个小缓冲区开始，随着更多解压缩数据的到来，当缓冲区被填满时，再分配一个更大的缓冲区，然后复制所有当前数据，再循环往复这个过程。

```javascript
let buffer = Buffer.alloc(64 * 1024); // Start with 64KB
let offset = 0;

function onData(chunk) {
  while (moreDataToCome) {
    if (offset + chunk.length > buffer.length) {
      // buffer full → allocate bigger one
      const newBuffer = Buffer.alloc(buffer.length * 2);

      // copy everything we’ve already written
      buffer.copy(newBuffer, 0, 0, offset);

      buffer = newBuffer;
    }

    // copy new chunk into buffer
    chunk.copy(buffer, offset);
    offset += chunk.length;
  }

  // ... decompress from buffer ...
}
```

这种处理逻辑看似合理，但会带来性能瓶颈：当缓冲区反复超出当前大小时，会出现多次复制拷贝相同数据的情况，举例来说，假设我们有一个 1M 大小的包，按照上述逻辑会经历以下步骤：
1. 初始化 64kb 大小的缓冲区
2. 填写 → 分配 128KB → 复制 64KB
3. 填写 → 分配 256KB → 复制 128KB
4. 填写 → 分配 512KB → 复制 256KB
5. 填写 → 分配 1MB → 复制 512KB

整个过程重复的复制了多达 960kb 的数据，而且每个安装包都会出现这种 case，对于比较大型的包，可能会复制相同的字节 5-6 次。

Bun 的处理方式则是在解压缩之前就缓冲整个 tarball，而不是在数据到达时才进行处理。它能做到这点是因为在 Zig 中可以直接查找到 tarball 文件的最后 4 个字节，这 4 个字节中存储了文件的未压缩大小，因此 Bun 可以预先分配内存。

```zig
{
  // Last 4 bytes of a gzip-compressed file are the uncompressed size.
  if (tgz_bytes.len > 16) {
    // If the file claims to be larger than 16 bytes and smaller than 64 MB, we'll preallocate the buffer.
    // If it's larger than that, we'll do it incrementally. We want to avoid OOMing.
    const last_4_bytes: u32 = @bitCast(tgz_bytes[tgz_bytes.len - 4 ..][0..4].*);
    if (last_4_bytes > 16 and last_4_bytes < 64 * 1024 * 1024) {
      // It's okay if this fails. We will just allocate as we go and that will error if we run out of memory.
      esimated_output_size = last_4_bytes;
      if (zlib_pool.data.list.capacity == 0) {
          zlib_pool.data.list.ensureTotalCapacityPrecise(zlib_pool.data.allocator, last_4_bytes) catch {};
      } else {
          zlib_pool.data.ensureUnusedCapacity(last_4_bytes) catch {};
      }
    }
  }
}
```

基于 Node.js 编写的包管理器很难做到这一点则是因为它需要单独创建一个读取流，一直搜索到最后，读取到那 4 个字节之后解析它们再关闭流，然后重新开始解压缩，这个过程会比流式传输更慢。

## 缓存友好的数据结构

在安装依赖包时，由于大多数包都有自己的依赖，且这些依赖还会有自己的依赖，就会形成一个比较复杂的图关系结构。包管理器必须遍历该图以检查包版本、解决版本冲突并确定要安装的版本，部分依赖项还需要进行"提升"，以便多个包可以共享它们。传统的包管理器存储依赖项的数据结构如下：
```javascript
const packages = {
  next: {
    name: "next",
    version: "15.5.0",
    dependencies: {
      "@swc/helpers": "0.5.15",
      "postcss": "8.4.31",
      "styled-jsx": "5.1.6",
    },
  },
  postcss: {
    name: "postcss",
    version: "8.4.31",
    dependencies: {
      nanoid: "^3.3.6",
      picocolors: "^1.0.0",
    },
  },
};
```
在 js 中，对象存储在堆上，当访问 `packages[“next”]` 时，CPU 会访问一个指针，该指针告诉它 Next 的数据在内存中的位置。然后，此数据包含指向其依赖项所在位置的另一个指针，而该指针又包含指向实际依赖项的更多指针。
![Pointer chasing through scattered JS objects in memory](https://bun.com/images/blog/bun-install/image24.png)

在不同时间创建对象时，javascript 引擎会使用当时可用的任何内存：
```javascript
// These objects are created at different moments during parsing
packages["react"] = { name: "react", ... }  	  // Allocated at address 0x1000
packages["next"] = { name: "next", ... }     		// Allocated at address 0x2000
packages["postcss"] = { name: "postcss", ... }  // Allocated at address 0x8000
// ... hundreds more packages
```
这些内存地址非常随机，没有任何局部性保证，对象可以随意分散在 RAM 中，即便是彼此有关联的对象！这种方式与现代 CPU 的取数机制背道而驰。

现代 CPU 处理数据的速度极快（每秒数十亿次运算），但从 RAM 获取数据的速度却很慢，为了弥补这一差距，CPU 实现了多级缓存：
* L1 缓存，32kb，但速度极快（~4 个 CPU 周期）
* L2 缓存，256kb，稍慢（~12 个 CPU 周期）
* L3 缓存，8-32MB 存储，需要 ~40 个 CPU 周期
* RAM：大 GB 空间存储，需要 ~300 个周期

当进行内存访问时，CPU 会加载该内存地址以及该地址后的整个 64 字节块，CPU 认为如果你访问了一个字节，那么你可能很快就会用到其附近的数据，这称之为空间局部性。这种机制非常适合按顺序存储的数据，像上面那种随机分配的内存地址就会适得其反。

当 CPU 在地址 0x2000 处加载 packages[“next”] 时，它实际上加载了该缓存行中的所有字节。但是下一个包 packages[“postcss”] 位于地址 0x8000 。这是一条完全不同的缓存线！CPU 加载在缓存行中的其他 56 字节完全被浪费了，它们只是附近恰好分配的任何东西的随机内存;也许是垃圾，也许是不相关对象的一部分。

当访问 512 个不同的包（32KB / 64 字节）时，L1 缓存会被填满。后续每个新的包访问都会逐出以前加载的缓存行以腾出空间。这样刚刚访问的包很快就会被逐出，缓存命中率下降，每次访问就都变成了 ~300 个周期的 RAM 行程，而不是 4 个周期的 L1 命中。

在遍历 Next 的依赖项时，CPU 必须执行多个依赖的内存加载：
1. 加载 packages[“next”] 指针 → 缓存未命中 → RAM 获取（~300 个周期）
2. 按照该指针加载 next.dependencies 指针 → 另一个缓存未命中 → RAM 获取（~300 个周期）
3. 按照它在哈希表中找到 “postcss” → 缓存未命中 → RAM 获取（~300 个周期）
4. 按照该指针加载实际字符串数据 → 缓存未命中 → RAM 获取（~300 个周期）

仅读取一个依赖项名称，就是 ~1200 个周期（在 400GHz CPU 上为 3ns），如果有 1000 个依赖包，每个包平均有 5 个依赖项，这就是 2 毫秒的纯内存延迟。

Bun 则采用了数组结构来存储所有的依赖项，将所有包名称保存在一个共享数组中：
```zig
// ❌ Traditional Array of Structures (AoS) - lots of pointers
packages = {
  next: { dependencies: { "@swc/helpers": "0.5.15", "postcss": "8.4.31" } },
};

// ✅ Bun's Structure of Arrays (SoA) - cache friendly
packages = [
  {
    name: { off: 0, len: 4 },
    version: { off: 5, len: 6 },
    deps: { off: 0, len: 2 },
  }, // next
];

dependencies = [
  { name: { off: 12, len: 13 }, version: { off: 26, len: 7 } }, // @swc/helpers@0.5.15
  { name: { off: 34, len: 7 }, version: { off: 42, len: 6 } }, // postcss@8.4.31
];

string_buffer = "next\015.5.0\0@swc/helpers\00.5.15\0postcss\08.4.31\0";
```



## 锁文件格式优化

## 文件复制优化

## 多核并行化

## 总结
