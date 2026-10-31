const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');
const { execFileSync } = require('node:child_process');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const rendererRequire = createRequire(require.resolve('hexo-renderer-marked'));
const { marked } = rendererRequire('marked');
const root = path.resolve(__dirname, '../..');
const sourcePath = path.join(root, 'source/_posts/claude-sonnet-opus.md');
const source = fs.readFileSync(sourcePath, 'utf8');
const markdown = source.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
const title = source.match(/^title:\s*(.+)$/m)[1];
const generatedAt = new Date();
const publishedLabel = `${String(generatedAt.getMonth() + 1).padStart(2, '0')}/${String(generatedAt.getDate()).padStart(2, '0')}`;
const out = __dirname;
const htmlPath = path.join(out, 'Claude模型对比-小红书版.html');
const imageDir = path.join(out, 'xiaohongshu');
const sourceImageDir = path.join(out, '.xhs-source-images');
const MAX_CONTENT_CARDS = 16;
const escapeHtml = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const visibleText = tokens => (tokens || []).map(token => token.type === 'br' ? '' : token.tokens ? visibleText(token.tokens) : token.text || '').join('');

const css = `
*{margin:0;padding:0;box-sizing:border-box;letter-spacing:0!important}
body{background:#454545;padding:90px 16px 40px;font-family:"PingFang SC","Microsoft YaHei",sans-serif;display:flex;flex-direction:column;align-items:center}
.toolbar{position:fixed;inset:0 0 auto;z-index:100;background:#1C1C1E;color:#F2EDE3;display:flex;justify-content:center;align-items:center;gap:12px;padding:12px;flex-wrap:wrap}
button,.toolbar a{font:13px "PingFang SC",sans-serif;color:#F2EDE3;background:#333;border:1px solid #888;padding:8px 12px;border-radius:6px;cursor:pointer;text-decoration:none}select{font-size:14px;padding:7px}#progress{font-size:12px}
.slide{width:540px;height:720px;position:relative;flex-shrink:0;margin-bottom:32px;overflow:hidden;background:#F2EDE3}
.bg-paper{position:absolute;inset:0;background:#F2EDE3}
.content{position:relative;height:100%;padding:32px 40px 24px;display:flex;flex-direction:column;color:#333}
.post-header{display:flex;align-items:center;gap:12px;margin-bottom:14px;flex-shrink:0;height:44px}
.avatar-wrap{position:relative;width:44px;height:44px;border:1.5px solid #C4956A;border-radius:50%;overflow:hidden;flex-shrink:0;background:#1C1C1E}
.avatar-fallback{position:absolute;inset:0;z-index:0;display:flex;align-items:center;justify-content:center;color:#F2EDE3;font-size:22px}.avatar-wrap img{position:absolute;inset:0;z-index:1;width:100%;height:100%;object-fit:cover;display:block}
.name{font-size:15px;font-weight:700;color:#1C1C1E}.date{font-size:13px;color:#888;margin-top:2px}
.post-body{height:566px;flex:1;min-height:0;overflow:hidden}.post-body p{font-size:18px;line-height:1.6;color:#333;margin-bottom:8px}.post-body strong{color:#1C1C1E;font-weight:700}.post-body em{color:#555}
.post-body .h1{font:800 27px/1.35 "Songti SC",serif;color:#1C1C1E;text-align:center;border-top:2px solid #1C1C1E;border-bottom:2px solid #1C1C1E;padding:14px 0;margin-bottom:20px}
.post-body .h2{font-size:22px;line-height:1.4;color:#1C1C1E;font-weight:700;border-left:4px solid #C4956A;padding-left:12px;margin-bottom:12px}.post-body .h3{font-size:19px;line-height:1.4;color:#2C2A28;font-weight:700;margin:4px 0 10px}
.list-item{display:flex;gap:8px;margin-bottom:7px;font-size:18px;line-height:1.6}.list-item .bullet{color:#999;font-weight:700;flex-shrink:0}.list-item.sub{margin-left:18px;font-size:16px}
code{background:#E8E0D1;color:#1C1C1E;padding:1px 5px;border-radius:4px;font-family:Menlo,monospace;font-size:.92em;white-space:nowrap}code.cmd-block{display:block;white-space:pre-wrap;word-break:break-word;padding:8px 12px;line-height:1.6}
.post-footer{padding-top:10px;border-top:1px solid #d8d1c6;display:flex;justify-content:space-between;align-items:center;flex-shrink:0;height:30px;color:#888;font-size:12px}.gz{color:#C4956A;font-weight:700}
.swipe-hint{font-size:12px;color:#aaa;text-align:center;padding-bottom:8px}.reading-note{font-size:12px;line-height:1.6;color:#888;margin-top:6px;padding-top:8px;border-top:1px solid #d8d1c6}
.cover .bg-paper,.closing .bg-paper{background:#1C1C1E}.cover .name,.closing .name{color:#F2EDE3}.cover .date,.closing .date{color:#aaa}.cover .post-body{display:flex;flex-direction:column;justify-content:center}.cover .post-body .h1{color:#F2EDE3;border-color:#C4956A}.cover .post-body p{color:#d8d1c6}.cover .post-footer,.closing .post-footer{color:#aaa;border-color:#444}.closing .post-body{display:flex;flex-direction:column;justify-content:center;gap:24px}.closing .q{font-size:18px;font-weight:400;line-height:1.7;color:#F2EDE3;padding-left:18px;border-left:3px solid #C4956A}.closing p{font-size:16px;color:#aaa;line-height:1.7}
.slide.img-only{height:auto;min-height:0;background:transparent;overflow:visible}.slide.img-only .bg-paper,.slide.img-only .post-header,.slide.img-only .post-footer{display:none}.slide.img-only .content{height:auto;padding:0}.slide.img-only .post-body{height:auto;overflow:visible}.slide.img-only img.main-img{display:block;width:540px;height:auto}
@media(max-width:570px){body{padding-left:0;padding-right:0}.slide{zoom:calc((100vw - 16px)/540px)}}
`;

function blocksFromMarkdown() {
  const blocks = [];
  let cursor = source.indexOf(markdown);
  const add = (html, kind, line, text, extra = {}) => blocks.push({ id: `block-${String(blocks.length + 1).padStart(3, '0')}`, kind, line, html, text, ...extra });
  for (const token of marked.lexer(markdown)) {
    const offset = source.indexOf(token.raw, cursor);
    const line = source.slice(0, offset).split('\n').length;
    cursor = offset + token.raw.length;
    if (['space', 'hr'].includes(token.type)) continue;
    if (token.type === 'heading') add(`<div class="h${token.depth}">${marked.parseInline(token.text)}</div>`, 'heading', line, visibleText(token.tokens), { depth: token.depth });
    else if (token.type === 'paragraph') {
      const imageToken = token.tokens?.find(part => part.type === 'image');
      if (imageToken) {
        const captionToken = token.tokens.find(part => part.type === 'em');
        add('', 'image', line, imageToken.text || '', { remoteUrl: imageToken.href });
        if (captionToken) add(`<p><em>${marked.parseInline(captionToken.text)}</em></p>`, 'caption', line + 1, visibleText(captionToken.tokens));
      } else add(`<p>${marked.parseInline(token.text)}</p>`, 'paragraph', line, visibleText(token.tokens));
    } else if (token.type === 'blockquote') {
      const text = token.text.replace(/\n/g, ' ');
      add(`<p>${marked.parseInline(text)}</p>`, 'quote', line, text);
    } else if (token.type === 'list') {
      let itemCursor = offset;
      token.items.forEach((item, index) => {
        const itemOffset = source.indexOf(item.raw, itemCursor);
        itemCursor = itemOffset + item.raw.length;
        const itemLine = source.slice(0, itemOffset).split('\n').length;
        const renderItem = (listItem, depth = 0) => {
          const textTokens = listItem.tokens.filter(part => part.type !== 'list' && part.type !== 'space');
          const text = textTokens.map(part => part.tokens ? visibleText(part.tokens) : part.text || '').join('');
          const inline = textTokens.map(part => marked.parseInline(part.text || '')).join('<br>');
          add(`<div class="list-item${depth ? ' sub' : ''}"><span class="bullet">${token.ordered ? `${token.start + index}.` : '•'}</span><div class="item-text">${inline}</div></div>`, 'list', itemLine, text);
          listItem.tokens.filter(part => part.type === 'list').forEach(list => list.items.forEach(child => renderItem(child, depth + 1)));
        };
        renderItem(item);
      });
    } else throw new Error(`Unsupported Markdown token: ${token.type} at line ${line}`);
  }
  return blocks;
}

function downloadImage(block, index) {
  fs.mkdirSync(sourceImageDir, { recursive: true });
  const rawPath = path.join(sourceImageDir, `${String(index + 1).padStart(2, '0')}-raw`);
  const pngPath = path.join(sourceImageDir, `${String(index + 1).padStart(2, '0')}-source.png`);
  if (!fs.existsSync(pngPath)) {
    execFileSync('curl', ['--fail', '--location', '--silent', '--show-error', block.remoteUrl, '--output', rawPath]);
    execFileSync('sips', ['-s', 'format', 'png', rawPath, '--out', pngPath], { stdio: 'ignore' });
    fs.rmSync(rawPath, { force: true });
  }
  return pngPath;
}

const downloadScript = `
const SCALE=2;
function flattenAlpha(canvas,bg){const flat=document.createElement('canvas');flat.width=canvas.width;flat.height=canvas.height;const context=flat.getContext('2d');context.fillStyle=bg;context.fillRect(0,0,flat.width,flat.height);context.drawImage(canvas,0,0);return flat;}
async function renderSlide(slide){await document.fonts.ready;await Promise.all(Array.from(slide.querySelectorAll('img')).map(image=>image.decode()));if(slide.classList.contains('img-only')){const image=slide.querySelector('.main-img');const canvas=document.createElement('canvas');canvas.width=image.naturalWidth;canvas.height=image.naturalHeight;canvas.getContext('2d').drawImage(image,0,0);return canvas;}const raw=await html2canvas(slide,{scale:SCALE,width:540,height:720,backgroundColor:null,useCORS:true,allowTaint:false,logging:false});return flattenAlpha(raw,slide.classList.contains('cover')||slide.classList.contains('closing')?'#1C1C1E':'#F2EDE3');}
function canvasToBlob(canvas){return new Promise((resolve,reject)=>canvas.toBlob(blob=>blob?resolve(blob):reject(new Error('PNG 导出失败')),'image/png'));}
async function downloadAll(){const progress=document.getElementById('progress');try{const slides=Array.from(document.querySelectorAll('.slide'));const zip=new JSZip();for(let index=0;index<slides.length;index++){progress.textContent='渲染 '+(index+1)+' / '+slides.length;zip.file('Claude模型对比-'+String(index+1).padStart(2,'0')+'.png',await canvasToBlob(await renderSlide(slides[index])));}saveAs(await zip.generateAsync({type:'blob'}),'Claude模型对比-小红书素材.zip');progress.textContent=slides.length+' 张已打包下载';}catch(error){progress.textContent='下载失败：'+error.message;alert(progress.textContent);throw error;}}
async function downloadOne(){const progress=document.getElementById('progress');const index=Number(document.getElementById('current').value);try{saveAs(await canvasToBlob(await renderSlide(document.getElementById('slide-'+index))),'Claude模型对比-'+String(index).padStart(2,'0')+'.png');progress.textContent='第 '+index+' 张已下载';}catch(error){progress.textContent='下载失败：'+error.message;alert(progress.textContent);throw error;}}
`;

async function paginate(page, blocks) {
  const firstTextIndex = blocks.findIndex(block => block.kind === 'paragraph');
  assert(firstTextIndex >= 0);
  const opening = blocks[firstTextIndex];
  const remaining = blocks.filter((_, index) => index !== firstTextIndex);
  await page.setContent(`<style>${css}</style><div class="slide"><div class="content"><div class="post-header"></div><div class="post-body"></div><div class="post-footer"></div></div></div>`);
  const result = await page.evaluate(({ input, maxCards }) => {
    const body = document.querySelector('.post-body');
    const parsed = input.map(block => {
      if (block.kind === 'image') return { ...block, fragments: [] };
      const holder = document.createElement('div'); holder.innerHTML = block.html;
      holder.querySelectorAll('code').forEach(element => { if (element.textContent.length > 26) element.classList.add('cmd-block'); });
      block.html = holder.innerHTML;
      const content = holder.querySelector('.item-text') || holder.firstElementChild;
      const text = content.textContent;
      const ends = [];
      if (['paragraph', 'quote', 'list'].includes(block.kind)) for (const match of text.matchAll(/[。！？](?:[”’」』）)]*)/g)) ends.push(match.index + match[0].length);
      if (!ends.length || ends.at(-1) !== text.length) ends.push(text.length);
      const nodes = []; let node; let offset = 0; const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT);
      while ((node = walker.nextNode())) { nodes.push({ node, start: offset, end: offset + node.length }); offset += node.length; }
      let start = 0; const fragments = [];
      for (const end of ends) {
        const first = nodes.find(entry => entry.end > start) || nodes.at(-1); const last = nodes.find(entry => entry.end >= end) || nodes.at(-1);
        const range = document.createRange(); range.setStart(first.node, start - first.start); range.setEnd(last.node, end - last.start);
        const piece = document.createElement('div'); piece.append(range.cloneContents()); fragments.push({ start, end, html: piece.innerHTML }); start = end;
      }
      return { ...block, text, fragments };
    });
    const slides = []; let placed = []; let stopped = false;
    const render = entries => entries.map(entry => {
      const block = parsed.find(candidate => candidate.id === entry.id); const holder = document.createElement('div'); holder.innerHTML = block.html;
      const target = holder.querySelector('.item-text') || holder.firstElementChild; target.innerHTML = entry.html;
      holder.firstElementChild.dataset.sourceBlock = entry.id; holder.firstElementChild.dataset.start = entry.start; holder.firstElementChild.dataset.end = entry.end; return holder.innerHTML;
    }).join('');
    const fits = (entries, reserve = 0) => { body.innerHTML = render(entries); const bounds = body.getBoundingClientRect(); const last = body.lastElementChild?.getBoundingClientRect(); return (!last || last.bottom <= bounds.bottom - reserve) && Array.from(body.querySelectorAll('*')).every(element => element.scrollWidth <= element.clientWidth + 1); };
    const append = (entries, block, fragment) => { const next = entries.map(entry => ({ ...entry })); if (next.at(-1)?.id === block.id) { next.at(-1).html += fragment.html; next.at(-1).end = fragment.end; } else next.push({ id: block.id, ...fragment }); return next; };
    for (let blockIndex = 0; blockIndex < parsed.length && !stopped; blockIndex++) {
      const block = parsed[blockIndex];
      if (block.kind === 'image') {
        if (placed.length) { slides.push({ type: 'text', entries: placed, html: render(placed) }); placed = []; }
        if (slides.length >= maxCards) { stopped = true; break; }
        slides.push({ type: 'image', blockId: block.id, remoteUrl: block.remoteUrl });
        if (slides.length >= maxCards && blockIndex < parsed.length - 1) stopped = true;
        continue;
      }
      for (const fragment of block.fragments) {
        let next = append(placed, block, fragment); let check = next;
        if (block.kind === 'heading') {
          let following = blockIndex + 1; while (parsed[following]?.kind === 'heading') { check = append(check, parsed[following], parsed[following].fragments[0]); following++; }
          if (parsed[following] && parsed[following].kind !== 'image') check = append(check, parsed[following], parsed[following].fragments[0]);
        }
        if (!fits(check, slides.length === maxCards - 1 ? 64 : 12)) {
          if (!placed.length) throw new Error('Source sentence exceeds one card: ' + block.id);
          slides.push({ type: 'text', entries: placed, html: render(placed) }); placed = [];
          if (slides.length >= maxCards) { stopped = true; break; }
          next = append(placed, block, fragment); if (!fits(next, slides.length === maxCards - 1 ? 64 : 12)) throw new Error('Cannot fit source fragment ' + block.id);
        }
        placed = next;
      }
    }
    if (placed.length && slides.length < maxCards) slides.push({ type: 'text', entries: placed, html: render(placed) });
    const consumed = new Set(slides.flatMap(slide => slide.type === 'image' ? [slide.blockId] : slide.entries.map(entry => entry.id)));
    const lastConsumedIndex = parsed.reduce((last, block, index) => consumed.has(block.id) ? index : last, -1);
    return { parsed, slides, truncated: stopped || lastConsumedIndex < parsed.length - 1 };
  }, { input: remaining, maxCards: MAX_CONTENT_CARDS });
  return { opening, ...result };
}

async function generate(page, blocks) {
  const report = await paginate(page, blocks);
  const avatar = `data:image/jpeg;base64,${fs.readFileSync(path.join(root, 'content/_shared/avatar.jpg')).toString('base64')}`;
  const header = `<div class="post-header"><div class="avatar-wrap"><span class="avatar-fallback">墨</span><img src="${avatar}" alt="墨筝"></div><div><div class="name">墨筝</div><div class="date">${publishedLabel}</div></div></div>`;
  const footer = number => `<div class="post-footer"><div>微信搜索公众号<span class="gz">「墨筝」</span>查看更多内容</div><div class="page">${number} / TOTAL</div></div>`;
  const wrap = (body, number, type = '') => `<div class="slide ${type}" id="slide-${number}"><div class="bg-paper"></div><div class="content">${header}<div class="post-body">${body}</div>${type === 'cover' ? '<div class="swipe-hint">← 左滑查看更多</div>' : ''}${footer(number)}</div></div>`;
  const openingHtml = report.opening.html.replace('<p>', `<p data-source-block="${report.opening.id}" data-start="0" data-end="${report.opening.text.length}">`);
  const cards = [wrap(`<div class="h1">${escapeHtml(title)}</div>${openingHtml}`, 1, 'cover')];
  const usedImages = [];
  report.slides.forEach(slide => {
    const number = cards.length + 1;
    if (slide.type === 'image') {
      const block = report.parsed.find(candidate => candidate.id === slide.blockId);
      const sourceIndex = blocks.filter(candidate => candidate.kind === 'image').findIndex(candidate => candidate.remoteUrl === block.remoteUrl);
      const localPath = downloadImage(block, sourceIndex);
      const imageData = `data:image/png;base64,${fs.readFileSync(localPath).toString('base64')}`;
      usedImages.push({ block, localPath, card: number });
      cards.push(`<div class="slide img-only" id="slide-${number}" data-source-block="${block.id}"><div class="content"><div class="post-body"><img class="main-img" src="${imageData}" alt="${escapeHtml(block.text)}"></div></div></div>`);
    } else {
      let body = slide.html;
      if (report.truncated && slide === report.slides.filter(item => item.type === 'text').at(-1)) body += '<div class="reading-note">完整内容请移步微信公众号「墨筝」阅读原文</div>';
      cards.push(wrap(body, number));
    }
  });
  const quote = '别人的评测数据只是参考，只有自己项目里的真实监控，才能给出最准确的答案。';
  assert(markdown.includes(quote));
  cards.push(wrap(`<div class="q">${quote}</div><p>微信搜索公众号「墨筝」<br>阅读完整原文</p>`, cards.length + 1, 'closing'));
  assert(cards.length <= 18);
  const dependencyNames = ['html2canvas', 'jszip', 'file-saver'];
  const dependencies = dependencyNames.map(name => {
    const cache = path.join(root, 'content/about-jev', `.xhs-${name}.js`); assert(fs.existsSync(cache), `Missing dependency cache: ${cache}`);
    return `<script>${fs.readFileSync(cache, 'utf8').replaceAll('</script', '<\\/script')}</script>`;
  }).join('\n');
  const options = cards.map((_, index) => `<option value="${index + 1}">第 ${index + 1} 张</option>`).join('');
  const html = `<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(title)}</title><style>${css}</style></head><body><div class="toolbar"><button onclick="downloadAll()">全部下载 (ZIP)</button><select id="current" aria-label="当前卡片">${options}</select><button onclick="downloadOne()">下载当前</button><a href="xiaohongshu/Claude模型对比-小红书素材.zip" download>已导出 ZIP</a><span id="progress"></span></div>${cards.join('\n').replaceAll('TOTAL', String(cards.length))}${dependencies}<script>${downloadScript}</script></body></html>`;
  fs.writeFileSync(htmlPath, html);
  const mapping = blocks.map(block => {
    let ranges = [];
    if (block.id === report.opening.id) ranges = [{ slide: 1, start: 0, end: block.text.length }];
    else if (block.kind === 'image') ranges = usedImages.filter(item => item.block.id === block.id).map(item => ({ slide: item.card, start: 0, end: 0 }));
    else ranges = report.slides.flatMap((slide, index) => slide.type === 'text' ? slide.entries.filter(entry => entry.id === block.id).map(entry => ({ slide: index + 2, start: entry.start, end: entry.end })) : []);
    const covered = ranges.at(-1)?.end || 0;
    return { id: block.id, kind: block.kind, depth: block.depth, source_line: block.line, original_text: block.text, remote_url: block.remoteUrl, ranges, status: block.kind === 'image' ? (ranges.length ? 'complete' : 'not_reached') : covered === block.text.length ? 'complete' : covered ? 'partial' : 'not_reached' };
  });
  const last = mapping.filter(block => block.ranges.length).at(-1);
  const sourceMap = { source: 'source/_posts/claude-sonnet-opus.md', title, card_count: cards.length, truncated: report.truncated, original_image_count: blocks.filter(block => block.kind === 'image').length, included_image_count: usedImages.length, last_source_block: last.id, last_source_line: last.source_line, coverage: mapping };
  fs.writeFileSync(path.join(out, 'xiaohongshu-source-map.json'), JSON.stringify(sourceMap, null, 2));
  return sourceMap;
}

async function validateAndExport(page, report) {
  await page.goto(pathToFileURL(htmlPath).href);
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all(Array.from(document.images).map(image => image.decode())); });
  const geometry = await page.evaluate(() => Array.from(document.querySelectorAll('.slide')).map(slide => {
    const body = slide.querySelector('.post-body'); const footer = slide.querySelector('.post-footer'); const bounds = body.getBoundingClientRect(); const imageOnly = slide.classList.contains('img-only');
    const children = Array.from(body.children).map(element => ({ top: element.getBoundingClientRect().top, bottom: element.getBoundingClientRect().bottom }));
    return { slide: slide.id, imageOnly, width: slide.getBoundingClientRect().width, height: slide.getBoundingClientRect().height, used: children.length ? children.at(-1).bottom - children[0].top : 0, overflow: !imageOnly && (body.scrollHeight > body.clientHeight + 1 || children.some(child => child.bottom > bounds.bottom + 1) || bounds.bottom > footer.getBoundingClientRect().top + 1), horizontal: Array.from(body.querySelectorAll('*')).some(element => element.scrollWidth > element.clientWidth + 1), fragments: Array.from(body.querySelectorAll('[data-source-block]')).map(element => ({ id: element.dataset.sourceBlock, start: Number(element.dataset.start), end: Number(element.dataset.end), text: (element.querySelector('.item-text') || element).textContent })) };
  }));
  assert.equal(geometry.length, report.card_count);
  geometry.forEach(slide => assert(!slide.overflow && !slide.horizontal, `Overflow: ${JSON.stringify(slide)}`));
  for (const slide of geometry) for (const fragment of slide.fragments) { const block = report.coverage.find(candidate => candidate.id === fragment.id); assert.equal(fragment.text, block.original_text.slice(fragment.start, fragment.end), `Text mismatch: ${fragment.id}`); }
  const headings = await page.locator('.h2,.h3').allTextContents(); headings.forEach(heading => assert(source.split('\n').some(line => line === `## ${heading}` || line === `### ${heading}`), `Invented heading: ${heading}`));
  const colors = await page.evaluate(() => ({ strong: [...new Set(Array.from(document.querySelectorAll('.post-body strong')).map(element => getComputedStyle(element).color))], h3: [...new Set(Array.from(document.querySelectorAll('.h3')).map(element => getComputedStyle(element).color))], bullet: [...new Set(Array.from(document.querySelectorAll('.bullet')).map(element => getComputedStyle(element).color))], paper: [...new Set(Array.from(document.querySelectorAll('.slide:not(.cover):not(.closing):not(.img-only) .bg-paper')).map(element => getComputedStyle(element).backgroundColor))] }));
  assert.deepEqual(colors.strong, ['rgb(28, 28, 30)']); if (colors.h3.length) assert.deepEqual(colors.h3, ['rgb(44, 42, 40)']); assert.deepEqual(colors.bullet, ['rgb(153, 153, 153)']); assert.deepEqual(colors.paper, ['rgb(242, 237, 227)']);
  fs.rmSync(imageDir, { recursive: true, force: true }); fs.mkdirSync(imageDir, { recursive: true });
  const pngs = [];
  for (let index = 1; index <= report.card_count; index++) {
    const result = await page.evaluate(async number => { const slide = document.getElementById('slide-' + number); const canvas = await renderSlide(slide); return { base64: canvas.toDataURL('image/png').split(',')[1], width: canvas.width, height: canvas.height, imageOnly: slide.classList.contains('img-only') }; }, index);
    if (!result.imageOnly) assert.deepEqual([result.width, result.height], [1080, 1440]);
    const filename = `Claude模型对比-${String(index).padStart(2, '0')}.png`; const buffer = Buffer.from(result.base64, 'base64'); fs.writeFileSync(path.join(imageDir, filename), buffer); pngs.push({ filename, base64: result.base64, width: result.width, height: result.height, imageOnly: result.imageOnly });
    console.log(`PNG ${index}/${report.card_count}: ${result.width}x${result.height}${result.imageOnly ? ' original image' : ''}`);
  }
  const zipData = await page.evaluate(async items => { const zip = new JSZip(); items.forEach(item => zip.file(item.filename, item.base64, { base64: true })); return zip.generateAsync({ type: 'base64', compression: 'DEFLATE' }); }, pngs);
  fs.writeFileSync(path.join(imageDir, 'Claude模型对比-小红书素材.zip'), Buffer.from(zipData, 'base64'));
  for (const number of [1, Math.min(8, report.card_count), report.card_count]) await page.locator(`#slide-${number}`).screenshot({ path: path.join(out, `xiaohongshu-check-${number}.png`) });
  await page.setViewportSize({ width: 390, height: 844 }); assert(await page.locator('#slide-1').evaluate(element => element.getBoundingClientRect().width <= 390));
  fs.writeFileSync(path.join(out, 'xiaohongshu-validation.json'), JSON.stringify({ passed: true, colors, geometry, png_count: pngs.length, exports: pngs.map(({ filename, width, height, imageOnly }) => ({ filename, width, height, imageOnly })), mobile: 'passed' }, null, 2));
}

async function main() {
  const blocks = blocksFromMarkdown(); assert.equal(blocks.filter(block => block.kind === 'image').length, 15);
  const browser = await chromium.launch({ headless: true, channel: 'chrome' }); const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
  const immutable = ['source/_posts/claude-sonnet-opus.md', 'content/claude-sonnet-opus/preview.html'].map(filename => [filename, fs.readFileSync(path.join(root, filename))]);
  try {
    const report = await generate(page, blocks); await validateAndExport(page, report);
    const copy = { title: 'Sonnet半价却更贵｜Claude选型', body: 'Sonnet 5.5 的输入输出单价只有 Opus 5.5 的一半，但把思考档位拉到 Max，单任务总成本反而可能贵一倍多。\n\n问题不在标价，而在隐藏的推理 Token。Sonnet 5.5 在高强度思考下平均输出约 19.3 万 Token，比 Opus 5.5 多近 60%。\n\n日常开发可以从 Sonnet 5.5 起步，用自动化检查把关；任务失败后升级到 Medium 档 Opus，而不是继续硬拉 Sonnet。复杂架构、跨仓库重构和高代价排错，则直接交给 Opus。\n\n完整跑分、接口变化和模型分工见公众号「墨筝」。', tags: ['AI', 'Claude', 'Sonnet', 'Opus', '模型选型', 'AI编程', 'ClaudeCode', 'Token成本', '开发者', '人工智能'] };
    assert(Array.from(copy.title).length <= 20); assert(Array.from(copy.body).length >= 150 && Array.from(copy.body).length <= 300); assert(copy.tags.length >= 8 && copy.tags.length <= 12);
    fs.writeFileSync(path.join(out, 'xiaohongshu-copy.md'), `# 小红书发布文案\n\n标题：${copy.title}\n\n${copy.body}\n\n.\n${copy.tags.map(tag => '#' + tag).join(' ')}\n`);
    const manifestPath = path.join(out, 'manifest.json'); const manifest = JSON.parse(fs.readFileSync(manifestPath)); const wechatBefore = JSON.stringify(manifest.outputs.wechat);
    manifest.outputs.xiaohongshu = { html: 'content/claude-sonnet-opus/Claude模型对比-小红书版.html', images_dir: 'content/claude-sonnet-opus/xiaohongshu', copy };
    assert.equal(JSON.stringify(manifest.outputs.wechat), wechatBefore); fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
    immutable.forEach(([filename, contents]) => assert(fs.readFileSync(path.join(root, filename)).equals(contents), `Modified immutable file: ${filename}`));
    console.log(JSON.stringify({ cards: report.card_count, included_images: report.included_image_count, original_images: report.original_image_count, truncated: report.truncated, last_source_line: report.last_source_line, copy_length: Array.from(copy.body).length, source_and_preview: 'unchanged', wechat_manifest: 'unchanged' }, null, 2));
  } finally { await browser.close(); }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
