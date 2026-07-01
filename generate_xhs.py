import re

html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>小红书版</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #2c2825;
    display: flex; flex-direction: column; align-items: center;
    padding: 90px 20px 80px;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif;
  }
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
  .content {
    position: relative; z-index: 2; height: 100%;
    padding: 32px 40px 24px; display: flex; flex-direction: column;
    color: #333; letter-spacing: 0.3px;
  }
  
  .slide[data-img-only="true"] { background: #1C1C1E; }
  .slide[data-img-only="true"] .bg-paper { display: none; }
  .slide[data-img-only="true"] .content { padding: 0; }
  .slide[data-img-only="true"] img.main-img {
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
    font-size: 19px; font-weight: 700; color: #2C2A28;
    margin-bottom: 10px; margin-top: 4px;
    letter-spacing: 0.5px;
  }

  .post-body p, .post-body blockquote { font-size: 18px; line-height: 1.6; margin-bottom: 12px; }
  .post-body em { font-style: italic; color: #555; }
  .post-body strong { color: #1C1C1E; font-weight: 700; }
  .post-body blockquote { border-left: 3px solid #ccc; padding-left: 10px; color: #555; font-size: 16px; }
  
  .list-item { display: flex; gap: 8px; margin-bottom: 7px; font-size: 18px; line-height: 1.6; }
  .list-item .bullet { color: #999; font-weight: bold; flex-shrink: 0; }
  
  code { background: #E8E0D1; color: #1C1C1E; padding: 1px 5px; border-radius: 4px; font-family: "SF Mono", Menlo, monospace; font-size: 0.92em; white-space: nowrap; }

  .post-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid rgba(28,28,30,0.08); flex-shrink: 0; }
  .post-footer .brand { font-size: 12px; color: #888; }
  .post-footer .brand .gz { color: #C4956A; font-weight: 700; }
  .post-footer .page { font-size: 12px; color: #888; }
  
  .swipe-hint {
    text-align: center; font-size: 12px; letter-spacing: 1px;
    margin-top: auto; padding-bottom: 8px; color: rgba(28,28,30,0.3);
  }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>
</head>
<body>
<div class="toolbar">
  <button class="btn accent" onclick="downloadAll()">全部下载 (ZIP)</button>
  <button class="btn" onclick="downloadOne()">下载当前</button>
  <span class="progress" id="progress"></span>
</div>
<div id="slides">
{slides_content}
</div>

<script>
// 同原代码的下载逻辑
const SCALE = 2;
function flattenAlpha(canvas, bgColor) {
  const flat = document.createElement('canvas');
  flat.width = canvas.width; flat.height = canvas.height;
  const ctx = flat.getContext('2d');
  ctx.fillStyle = bgColor; ctx.fillRect(0, 0, flat.width, flat.height);
  ctx.drawImage(canvas, 0, 0);
  return flat;
}
async function renderSlide(s) {
  const origRadius = s.style.borderRadius; s.style.borderRadius = '0';
  const isImgOnly = s.getAttribute('data-img-only') === 'true';
  const bg = isImgOnly ? '#1C1C1E' : '#F2EDE3';
  const raw = await html2canvas(s, { scale: SCALE, useCORS: true, allowTaint: false, backgroundColor: null, width: 540, height: 720, logging: false });
  s.style.borderRadius = origRadius;
  return flattenAlpha(raw, bg);
}
function canvasToBlob(c) { return new Promise(r => c.toBlob(r, 'image/png')); }
async function downloadAll() {
  const slides = document.querySelectorAll('.slide');
  const zip = new JSZip();
  for (let i = 0; i < slides.length; i++) {
    const canvas = await renderSlide(slides[i]);
    const blob = await canvasToBlob(canvas);
    zip.file(`小红书-${String(i+1).padStart(2,'0')}.png`, blob);
  }
  saveAs(await zip.generateAsync({type:'blob'}), '小红书轮播图.zip');
}
</script>
</body>
</html>
"""

def generate():
    with open('source/_posts/glm-vs-kimi-code-benchmark.md', 'r') as f:
        md = f.read()

    blocks = md.split('\n\n')
    slides_html = ""
    slide_index = 1
    
    def start_slide(pageNum):
        return f'<div class="slide" id="slide-{pageNum}"><div class="bg-paper"></div><div class="content">' + \
               f'<div class="post-header"><div class="avatar-wrap">筝</div><div class="meta"><div class="name">墨筝</div><div class="date">2026-06-18</div></div></div><div class="post-body">'
    
    def end_slide(pageNum):
        return f'</div><div class="swipe-hint">左滑阅读更多</div><div class="post-footer"><div class="brand">首发自公众号 <span class="gz">墨筝 MOZHENG</span></div><div class="page">{pageNum}</div></div></div></div>\n'
    
    current_content = ""
    slides = []
    
    for block in blocks:
        block = block.strip()
        if not block or block.startswith('---'): continue
        if block.startswith('title:'):
            title = block.replace('title: ', '')
            current_content += f'<div class="h1">{title}</div>'
            continue
        if block.startswith('date:') or block.startswith('tags:') or block.startswith('categories:') or block.startswith('- Benchmark') or block.startswith('- AI编程') or block.startswith('- GLM') or block.startswith('- Kimi'):
            continue
        if block.startswith('![]'):
            # It's an image block. Push current content then image slide
            if current_content:
                slides.append(current_content)
                current_content = ""
            img_url = block.replace('![](', '').replace(')', '')
            slides.append(f'<img src="{img_url}" class="main-img" crossorigin="anonymous">')
            continue

        # basic formatting
        block = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', block)
        block = re.sub(r'`(.*?)`', r'<code>\1</code>', block)

        if block.startswith('## '):
            html_block = f'<div class="h2">{block[3:]}</div>'
        elif block.startswith('### '):
            html_block = f'<div class="h3">{block[4:]}</div>'
        elif block.startswith('> '):
            html_block = f'<blockquote>{block[2:]}</blockquote>'
        elif block.startswith('- '):
            items = block.split('\n')
            html_block = ""
            for item in items:
                html_block += f'<div class="list-item"><span class="bullet">•</span><div>{item[2:]}</div></div>'
        else:
            html_block = f'<p>{block}</p>'
        
        current_content += html_block + "\n"

        # very naive length based splitting
        if len(current_content) > 360:
            slides.append(current_content)
            current_content = ""

    if current_content:
        slides.append(current_content)
        
    slides_str = ""
    page = 1
    
    # insert specific Xiaohei images at correct positions!
    # They should probably be inserted right after certain pages.
    # 01-planning-vs-building.png -> after 为什么现在的分水岭是规划能力
    # 02-hash-bucket.png -> after 灰度发布的隐蔽陷阱
    # 03-cache-miss.png -> after Planning 阶段：GLM 更强的工程判断力
    
    # Actually, we can just look inside the content for these headers, and insert an image slide.
    
    for s_idx, s in enumerate(slides):
        if s.startswith('<img '):
            slides_str += f'<div class="slide" data-img-only="true" id="slide-{page}"><div class="bg-paper"></div><div class="content">{s}</div></div>\n'
            page += 1
        else:
            slides_str += start_slide(page) + s + end_slide(page)
            page += 1
            
            if '为什么规划能力是模型分水岭' in s or ('大概率也能让曹仁灰头土脸' in s):
                slides_str += f'<div class="slide" data-img-only="true" id="slide-{page}"><div class="bg-paper"></div><div class="content"><img src="xiaohei-illustrations/01-planning-vs-building.png" class="main-img"></div></div>\n'
                page += 1
            if '灰度发布的隐蔽陷阱' in s or ('功能不能得而复失' in s):
                slides_str += f'<div class="slide" data-img-only="true" id="slide-{page}"><div class="bg-paper"></div><div class="content"><img src="xiaohei-illustrations/02-hash-bucket.png" class="main-img"></div></div>\n'
                page += 1
            if 'GLM 判断更强' in s or ('清空之前的缓存' in s) or ('没有任何安全收益' in s):
                slides_str += f'<div class="slide" data-img-only="true" id="slide-{page}"><div class="bg-paper"></div><div class="content"><img src="xiaohei-illustrations/03-cache-miss.png" class="main-img"></div></div>\n'
                page += 1

    final_html = html_template.replace('{slides_content}', slides_str)
    
    with open('content/glm-vs-kimi-code-benchmark/glm-vs-kimi-code-benchmark-小红书版.html', 'w') as f:
        f.write(final_html)

generate()
