# -*- coding: utf-8 -*-
import base64, os

# 预先把头像 base64 内嵌，避免 file:// 下 html2canvas 污染 canvas
AVATAR_PATH = "content/_shared/avatar.jpg"
if os.path.exists(AVATAR_PATH):
    with open(AVATAR_PATH, "rb") as f:
        AVATAR_DATA_URI = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
else:
    AVATAR_DATA_URI = ""

template = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>Claude Opus 4.8 - 小红书 (v4 - 含下载工具栏)</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #2c2825;
    display: flex; flex-direction: column; align-items: center;
    padding: 90px 20px 80px;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif;
  }
  /* ===== 下载工具栏 ===== */
  .toolbar {
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    background: rgba(28,28,30,0.95); backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding: 12px 20px; display: flex; align-items: center;
    justify-content: center; gap: 12px;
  }
  .toolbar .btn {
    background: #1C1C1E; color: #F2EDE3; border: 1px solid rgba(255,255,255,0.15);
    padding: 9px 22px; border-radius: 8px; font-size: 13px;
    font-weight: 600; cursor: pointer;
  }
  .toolbar .btn.accent { background: #C4956A; border-color: #C4956A; }
  .toolbar .progress { color: rgba(255,255,255,0.7); font-size: 12px; margin-left: 8px; }

  .slide {
    width: 540px; height: 720px; margin-bottom: 40px;
    position: relative; overflow: hidden; border-radius: 8px;
    box-shadow: 0 6px 28px rgba(28,28,30,0.35); background: #fff;
  }
  .bg-paper {
    position: absolute; inset: 0;
    background: linear-gradient(135deg, #F6F1E7 0%, #F2EDE3 55%, #ECE4D2 100%);
  }
  .bg-paper::after {
    content: ''; position: absolute; inset: 0; opacity: 0.04;
    background-image: linear-gradient(rgba(28,28,30,0.6) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(28,28,30,0.6) 1px, transparent 1px);
    background-size: 28px 28px; pointer-events: none;
  }
  .bg-paper::before {
    content: ''; position: absolute; right: -60px; top: -60px;
    width: 240px; height: 240px; border-radius: 50%;
    background: radial-gradient(circle, rgba(196,149,106,0.18) 0%, transparent 70%);
    pointer-events: none;
  }
  .content {
    position: relative; z-index: 2; height: 100%;
    padding: 32px 40px 24px; display: flex; flex-direction: column;
    color: #333; letter-spacing: 0.3px;
  }
  
  /* Pure-image slide: no chrome, just an image filling the card */
  .slide.img-only { background: #1C1C1E; }
  .slide.img-only .bg-paper { display: none; }
  .slide.img-only .content { padding: 0; }
  .slide.img-only img.main-img {
    width: 100%; height: 100%; object-fit: contain; display: block;
  }

  .post-header { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; flex-shrink: 0; }
  .avatar-wrap { width: 44px; height: 44px; border-radius: 50%; border: 1.5px solid #C4956A; overflow: hidden; background: linear-gradient(135deg, #C4956A, #8a6240); flex-shrink: 0; display: flex; align-items: center; justify-content: center; color: #F2EDE3; font-weight: 700; font-family: "Songti SC", serif; font-size: 18px; }
  .avatar-wrap img { width: 100%; height: 100%; object-fit: cover; }
  .meta .name { font-size: 15px; font-weight: 700; color: #1C1C1E; }
  .meta .date { font-size: 13px; color: #888; margin-top: 2px; }

  .post-body { flex: 1; overflow: hidden; }
  
  .post-body .h1 {
    font-size: 27px; font-weight: 800; color: #1C1C1E;
    margin-bottom: 16px; line-height: 1.35;
    text-align: center; padding: 12px 0;
    border-top: 2px solid #1C1C1E; border-bottom: 2px solid #1C1C1E;
    font-family: "Songti SC", "Source Han Serif SC", serif;
    letter-spacing: 1px;
  }
  .post-body .h2 {
    font-size: 22px; font-weight: 700; color: #1C1C1E;
    margin-bottom: 12px; border-left: 4px solid #C4956A; padding-left: 12px;
  }
  .post-body .h3 {
    font-size: 19px; font-weight: 700; color: #C4956A;
    margin-bottom: 10px; margin-top: 4px;
    letter-spacing: 0.5px;
  }

  .post-body p { font-size: 18px; line-height: 1.6; margin-bottom: 8px; }
  .post-body em { font-style: italic; color: #555; }
  .post-body strong { color: #C4956A; font-weight: 600; }
  
  .list-item { display: flex; gap: 8px; margin-bottom: 7px; font-size: 18px; line-height: 1.6; }
  .list-item .bullet { color: #C4956A; font-weight: bold; flex-shrink: 0; }
  .list-item.sub { margin-left: 18px; font-size: 16px; }
  
  .table-block { background: #f5efe4; border: 1px solid #e8dfd0; border-radius: 8px; padding: 10px 14px; margin-bottom: 10px; }
  .table-row { border-bottom: 1px dashed rgba(196,149,106,0.4); padding: 6px 0; font-size: 15.5px; }
  .table-row:first-child { padding-top: 0; }
  .table-row:last-child { border-bottom: none; padding-bottom: 0; }
  .table-row .key { font-weight: 700; color: #1C1C1E; margin-bottom: 2px; font-size: 16px; }
  .table-row .val { color: #555; line-height: 1.5; }
  
  code { background: #E8E0D1; color: #b8621b; padding: 1px 5px; border-radius: 4px; font-family: "SF Mono", Menlo, monospace; font-size: 0.92em; white-space: nowrap; }
  code.cmd-block { display: block; white-space: pre-wrap; word-break: break-word; padding: 8px 12px; margin-top: 6px; line-height: 1.55; }

  .post-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid rgba(28,28,30,0.08); flex-shrink: 0; }
  .post-footer .brand { font-size: 12px; color: #888; }
  .post-footer .brand .gz { color: #C4956A; font-weight: 700; }
  .post-footer .page { font-size: 12px; color: #888; }
  
  .quote-card { flex: 1; display: flex; flex-direction: column; justify-content: center; }
</style>
</head>
<body>
<div class="toolbar">
  <button class="btn accent" onclick="downloadAll()">全部下载 (ZIP)</button>
  <button class="btn" onclick="downloadOne()">下载当前</button>
  <span class="progress" id="progress"></span>
</div>
{content}

<!-- ===== 自动写入今天的日期 ===== -->
<script>
  (function(){
    const d = new Date();
    const mm = String(d.getMonth()+1).padStart(2,'0');
    const dd = String(d.getDate()).padStart(2,'0');
    document.querySelectorAll('.date').forEach(el => el.textContent = `${mm}/${dd}`);
  })();
</script>

<!-- ===== 下载脚本 ===== -->
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>
<script>
const SCALE = 2;
function flattenAlpha(canvas, bgColor) {
  const isTransparent = !bgColor || bgColor === 'transparent' || bgColor === 'rgba(0, 0, 0, 0)';
  const flat = document.createElement('canvas');
  flat.width = canvas.width; flat.height = canvas.height;
  const ctx = flat.getContext('2d');
  ctx.fillStyle = isTransparent ? '#F2EDE3' : bgColor;
  ctx.fillRect(0, 0, flat.width, flat.height);
  ctx.drawImage(canvas, 0, 0);
  return flat;
}

// 预把跨域图片转成 dataURL，避免 html2canvas 因为 CORS 把 canvas 标 tainted。
async function fetchAsDataURL(url) {
  const r = await fetch(url, { mode: 'cors', cache: 'force-cache' });
  if (!r.ok) throw new Error('HTTP ' + r.status);
  const blob = await r.blob();
  return await new Promise((res, rej) => {
    const fr = new FileReader();
    fr.onload = () => res(fr.result);
    fr.onerror = rej;
    fr.readAsDataURL(blob);
  });
}

async function inlineRemoteImages() {
  const imgs = Array.from(document.querySelectorAll('img'));
  await Promise.all(imgs.map(async (img) => {
    const src = img.getAttribute('src') || '';
    if (!src || src.startsWith('data:') || src.startsWith('blob:')) return;
    try {
      const u = new URL(src, location.href);
      if (u.origin === location.origin) return;
    } catch (_) { return; }

    // 候选下载源：直连 → weserv 代理（自动加 CORS 头）→ corsproxy.io
    const stripped = src.replace(/^https?:\/\//, '');
    const candidates = [
      src,
      'https://wsrv.nl/?url=' + encodeURIComponent(stripped),
      'https://images.weserv.nl/?url=' + encodeURIComponent(stripped),
      'https://corsproxy.io/?' + encodeURIComponent(src),
    ];

    let dataUrl = null, lastErr = null;
    for (const u of candidates) {
      try { dataUrl = await fetchAsDataURL(u); break; }
      catch (e) { lastErr = e; }
    }

    if (dataUrl) {
      img.src = dataUrl;
      if (img.decode) { try { await img.decode(); } catch (_) {} }
    } else {
      // 所有源都失败，把图片替换为 1x1 透明占位，避免污染 canvas
      console.warn('图片所有下载源都失败，将替换为占位符：', src, lastErr);
      img.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
      img.style.background = '#ddd';
      img.dataset.failed = '1';
    }
  }));
}

async function renderSlide(s) {
  const origRadius = s.style.borderRadius;
  s.style.borderRadius = '0';
  const isImgOnly = s.classList.contains('img-only');
  const bg = isImgOnly ? '#1C1C1E' : '#F2EDE3';
  const raw = await html2canvas(s, { scale: SCALE, useCORS: true, allowTaint: false, backgroundColor: null, width: 540, height: 720, logging: false });
  s.style.borderRadius = origRadius;
  return flattenAlpha(raw, bg);
}
function canvasToBlob(c) { return new Promise(r => c.toBlob(r, 'image/png')); }

async function downloadAll() {
  const progress = document.getElementById('progress');
  try {
    progress.textContent = '预加载图片...';
    await inlineRemoteImages();
    const slides = document.querySelectorAll('.slide');
    const zip = new JSZip();
    for (let i = 0; i < slides.length; i++) {
      progress.textContent = `渲染第 ${i+1}/${slides.length} 张...`;
      const canvas = await renderSlide(slides[i]);
      const blob = await canvasToBlob(canvas);
      if (!blob) throw new Error(`第 ${i+1} 张 toBlob 失败（canvas 可能被跨域污染）`);
      zip.file(`小红书-${String(i+1).padStart(2,'0')}.png`, blob);
    }
    progress.textContent = '打包中...';
    saveAs(await zip.generateAsync({type:'blob'}), '小红书轮播图.zip');
    progress.textContent = `${slides.length} 张已打包下载`;
  } catch (e) {
    console.error(e);
    progress.textContent = '下载失败：' + (e && e.message ? e.message : e);
    alert('下载失败：' + (e && e.message ? e.message : e) + '\n请打开浏览器控制台查看详情。');
  }
}

async function downloadOne() {
  const progress = document.getElementById('progress');
  try {
    await inlineRemoteImages();
    const slides = document.querySelectorAll('.slide');
    const vc = window.innerHeight / 2;
    let idx = 0, min = Infinity;
    slides.forEach((s,i) => {
      const d = Math.abs(s.getBoundingClientRect().top + 360 - vc);
      if (d < min) { min = d; idx = i; }
    });
    const canvas = await renderSlide(slides[idx]);
    const blob = await canvasToBlob(canvas);
    if (!blob) throw new Error('toBlob 失败（canvas 可能被跨域污染）');
    saveAs(blob, `小红书-${String(idx+1).padStart(2,'0')}.png`);
  } catch (e) {
    console.error(e);
    progress.textContent = '下载失败：' + (e && e.message ? e.message : e);
    alert('下载失败：' + (e && e.message ? e.message : e));
  }
}
</script>
</body>
</html>"""

def slide(html, page, total, img_only=False):
    if img_only:
        return f"""<div class="slide img-only" id="slide-{page}"><div class="bg-paper"></div><div class="content">{html}</div></div>"""
    return f"""<div class="slide" id="slide-{page}">
  <div class="bg-paper"></div>
  <div class="content">
    <div class="post-header">
      <div class="avatar-wrap"><img src="__AVATAR__" onerror="this.parentNode.innerHTML='墨'"></div>
      <div class="meta"><div class="name">墨筝</div><div class="date">06/01</div></div>
    </div>
    <div class="post-body">{html}</div>
    <div class="post-footer">
      <div class="brand">微信搜索公众号<span class="gz">「墨筝」</span>查看更多内容</div>
      <div class="page">{page} / {total}</div>
    </div>
  </div>
</div>"""

slide_contents = [
    {"html": """
    <div class="h1">Claude Opus 4.7 升级到 4.8<br>对用户来说带来了哪些改变?</div>
    <p>Opus 4.8 相比 4.7 除了基础 benchmark 跑分的提升以外，还带来了对用户而言更有用的三大工程特性：<strong>算力控制（Effort control）</strong>、<strong>极速模式（Fast mode）</strong>以及<strong>动态工作流（Dynamic workflows）</strong>。</p>
    <p>用好这些功能不仅能获得更惊艳的代码生成，还能极大地节省开销。</p>
    """},
    {"img_only": True, "html": """<img class="main-img" src="https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBjKVqHjShtN6NeK5v71YJYyFnpDwLTAACcA1rG_fF8ESnmm2Zg6q9GQEAAwIAA3cAAzsE.jpeg" alt="benchmark">"""},
    {"html": """
    <div class="h2">跑分情况</div>
    <div class="list-item"><span class="bullet">•</span><div><strong>代码能力</strong></div></div>
    <div class="list-item sub"><span class="bullet">-</span><div>SWE-bench Verified：87.6% → 88.6%（已非常接近当前天花板）。</div></div>
    <div class="list-item sub"><span class="bullet">-</span><div>SWE-bench Pro（难度更高，数据污染更少）：从 64.3% 爆拉至 69.2%，领先 GPT-5.5 超 10 个百分点。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><strong>命令行工具（Terminal）</strong></div></div>
    <div class="list-item sub"><span class="bullet">-</span><div>Terminal-Bench 2.1：66.1% → 74.6%（提升 8.5）。但值得注意的是，GPT-5.5 依然以 78.2% 的成绩保持领先，这是 Opus 4.8 在核心测试中唯一落后的一项。</div></div>
    """},
    {"html": """
    <div class="list-item"><span class="bullet">•</span><div><strong>知识型工作</strong></div></div>
    <div class="list-item sub"><span class="bullet">-</span><div>GDPval-AA：Opus 4.8 为 1890 Elo，GPT-5.5 为 1769，是整张对比表里差距最大的一项。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><strong>计算机使用</strong>（模型在真实界面里完成操作任务的能力，例如点按钮、填表单、切换页面并按步骤执行流程）</div></div>
    <div class="list-item sub"><span class="bullet">-</span><div>OSWorld-Verified：83.4%。其中一部分提升来自测试框架本身的更新，Anthropic 也在发布说明中明确标注了这一点。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><strong>科学推理</strong></div></div>
    <div class="list-item sub"><span class="bullet">-</span><div>GPQA Diamond：93.6%，与上一代基本持平。两代模型都稳定在 93% 以上，更接近指标饱和，而不是能力回退。</div></div>
    """},
    {"html": """
    <div class="h2">三大特性</div>
    <div class="h3">特性一：省钱利器之算力控制</div>
    <p>默认情况下，Opus 4.8 会停留在"High（高算力）"级别。你可以精准掌控具体任务投入多少算力，做到极致 ROI。以 Claude Code 为例，用 <code>/effort</code> 命令调节，五档区分如下：</p>
    <div class="list-item"><span class="bullet">•</span><div><code>/effort low</code>：快速问答、改改格式，Token 消耗极低。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><code>/effort medium</code>：日常常规编辑和代码起草。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><code>/effort high</code>：提供扎实稳定的推理结构。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><code>/effort xhigh</code>：复杂代码深入分析与多步代理操作。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><code>/effort max</code>：算力全开，当前会话无 Token 上限。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><code>/effort auto</code>：让模型自适应思考。</div></div>
    <p style="margin-top:10px;">所有级别 token 基础单价相同（输入 $5 / 输出 $25 每百万 Tokens），核心差异在于实际"思考"的时间长短与 Token 生成数量。</p>
    """},
    {"html": """
    <p>Max 级别之所以更贵，主要是因为它在深度思考时消耗了更多的 Token 总量。</p>
    <div class="table-block">
      <div class="table-row"><div class="key">Low · 极简 minimal · ~0.1x</div><div class="val">细枝末节、格式化梳理、简单提问</div></div>
      <div class="table-row"><div class="key">Medium · 适中 moderate · ~0.4x</div><div class="val">常规代码修改、草案编写、核心摘要</div></div>
      <div class="table-row"><div class="key">High · 扎实 solid · 1x (基准)</div><div class="val">日常编码主力、代码审查 (默认档)</div></div>
      <div class="table-row"><div class="key">Extra (xhigh) · 深入 deeper · ~2-3x</div><div class="val">复杂逻辑代码、Agent 代理、长线任务</div></div>
      <div class="table-row"><div class="key">Max · 极限 maximum · ~4-8x</div><div class="val">重型底层架构、攻坚最棘手的疑难杂症</div></div>
    </div>
    <p style="margin-top:10px;">默认 High 模式下一条回答约 $0.05，切到 Low 只需约 $0.005，而开到 Max 则会轻易飙升至 $0.20 - $0.40。大多数人都是直接挂默认 High，极少主动调节，但不同任务适合不同算力水准，认真抠一抠能省不少钱。</p>
    """},
    {"html": """
    <div class="h3">特性二：心流专属之极速模式</div>
    <p>极速模式（Fast Mode）能让 4.8 在基本不降低输出质量的情况下以 <strong>2.5 倍</strong>的速度冲刺运行，并且同 fast 模式还降价到了以前的三分之一。</p>
    <div class="list-item"><span class="bullet">•</span><div><strong>标准 Opus 4.8</strong>：$5 / $25 每百万 Tokens</div></div>
    <div class="list-item"><span class="bullet">•</span><div><strong>极速 Opus 4.8</strong>：$10 / $50 每百万 Tokens（速度 2.5x）<em>（老版本高达 $30 / $150）</em></div></div>
    <p style="margin-top:8px;">在 Claude Code 中通过输入 <code>/fast</code> 即可开启。</p>
    <p style="margin-top:10px;"><strong>适合心流场景</strong>：根据需求文档直接生成大量代码、补充技术文档或基础单元测试。</p>
    <p style="margin-top:8px;"><strong>慎用场景</strong>：复杂 Debug、底层架构决策、安全漏洞审查。极速模式为保证低延迟，不太支持耗时较长的深度逻辑推演与不断自我证伪。</p>
    """},
    {"html": """
    <div class="h3">特性三：省心高效之动态工作流（the big thing）</div>
    <p>对于大型任务，Claude Code 现在会自动编写一段 JavaScript 编排脚本，并在后台静默执行。终端不会被长期 block，随时能响应前台任务；整个执行计划被抽离成了本地代码以后，也不用再担心冗长的过程会撑爆模型上下文，只需要感知其执行结果即可。</p>
    <p style="margin-top:10px;">关于其运作机制，可以参考如下：</p>
    <div class="list-item"><span class="bullet">•</span><div><strong>16 个子 agent 并发</strong>：最多同时运行 16 个 Subagent，且单次运行有 1000 个任务上限，避免失控。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><strong>断点续执行</strong>：运行中途断电或终端关闭，下次重连会自动接续断点，无需推倒重来。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><strong>权限白名单</strong>：所有 Subagent 默认开启 <code>acceptEdits</code>，但严格遵循之前设定的权限。</div></div>
    """},
    {"img_only": True, "html": """<img class="main-img" src="https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBjKlqHjgVCKnsUnPy42pU2yRar6o2bQACdA1rG_fF8ESmVxYFgKkGkgEAAwIAA3cAAzsE.png" alt="动态工作流示意">"""},
    {"html": """
    <div class="list-item"><span class="bullet">•</span><div><strong>门槛与开启方式</strong>：首先本地 Claude Code 需要升到 v2.1.154+。Max、Team 或 Enterprise 会员等级下会默认生效，只是普通的 Pro 档，则需手动切到 Opus 4.8 并在 <code>/config</code> 中自行勾选开启。</div></div>
    <div class="list-item"><span class="bullet">•</span><div><strong>触发方式</strong>：功能开启后，先执行 <code>/effort&nbsp;ultracode</code>，再用一句自然语言直接下达任务。例如：<code class="cmd-block">/effort ultracode 审核 src/routes/ 目录下所有接口的鉴权逻辑，补上所有漏洞。</code></div></div></div></div>
    """},
    {"html": """
    <div class="h2">使用建议</div>
    <p>动态工作流比较适合高复杂度、覆盖面广的任务，比如跨 200+ 文件的迁移改造、全项目安全 review、以及大规模重构与补测。在这类场景中，多任务并行能显著提升工作效率。</p>
    <p style="margin-top:14px;">如果只是单文件的小修小改或常规问答，就别用了，多 Agent 协同不仅会显著增加 Token 消耗，也有点杀鸡用牛刀。</p>
    <p style="margin-top:14px;">官方给出的建议是先小范围试跑，再决定是否全量执行：先在一个子目录发起任务，观察实际触发的子代理规模与 Token 开销，最后再评估全仓运行的成本和收益。</p>
    <p style="margin-top:14px;"><em>如需完全禁用动态工作流，可设置环境变量：</em></p>
    <p><code>export CLAUDE_CODE_DISABLE_WORKFLOWS=1</code></p>
    """},
    {"html": """
    <div class="h2">写在最后</div>
    <div class="quote-card">
      <p style="font-size:17px; line-height:1.85; color:#333;">从 Opus 4.7 到 4.8，除了模型本身的更新迭代，Claude 还做了一些工程能力上的升级。</p>
      <p style="font-size:17px; line-height:1.85; color:#333; margin-top:20px;">对于用户来说，在模型代际并无突破式更新的情况下，工程能力的升级<span style="color:#C4956A; font-weight:700;">往往比模型本身更有实用价值</span>。</p>
    </div>
    """}
]

final_html = ""
total = len(slide_contents)
for i, c in enumerate(slide_contents):
    final_html += slide(c["html"], i+1, total, c.get("img_only", False))

output = template.replace("{content}", final_html).replace("__AVATAR__", AVATAR_DATA_URI)

# 1. 写入实际帖子产物
with open("content/opus4.8-opus4.7/opus4.8-opus4.7-小红书版.html", "w") as f:
    f.write(output)

# 2. 同步保存为新版 reference 范例（仅含模板结构 + 前3张示例 slide）
sample_slides = "".join([
    slide(slide_contents[0]["html"], 1, 3),
    slide(slide_contents[2]["html"], 2, 3, img_only=True),
    slide(slide_contents[7]["html"], 3, 3),
])
ref = template.replace("{content}", sample_slides).replace("__AVATAR__", AVATAR_DATA_URI).replace(
    "<title>Claude Opus 4.8 - 小红书 (v4 - 含下载工具栏)</title>",
    "<title>小红书 Markdown 还原范例 v2（h1/h2/h3 + 图片独占 + 下载工具栏）</title>")
with open(".agents/skills/content-pipeline/references/xiaohongshu-examples/markdown-faithful-范例.html", "w") as f:
    f.write(ref)

print(f"Generated {total} slides + reference example.")
