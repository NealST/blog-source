const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');
const { chromium } = require('playwright');
const { execFileSync } = require('node:child_process');
const rendererRequire = createRequire(require.resolve('hexo-renderer-marked'));
const { marked } = rendererRequire('marked');
const root = path.resolve(__dirname, '../..');
const source = fs.readFileSync(path.join(root, 'source/_posts/about-jev.md'), 'utf8');
const markdown = source.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');

const title = source.match(/^title:\s*(.+)$/m)[1];
const publishedAt = new Date(source.match(/^date:\s*(.+)$/m)[1]);
const publishedLabel = `${String(publishedAt.getMonth() + 1).padStart(2, '0')}/${String(publishedAt.getDate()).padStart(2, '0')}`;
const out = __dirname;
const htmlPath = path.join(out, 'Jev-小红书版.html');
const imageDir = path.join(out, 'xiaohongshu');
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
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
.avatar-wrap .avatar-fallback{position:absolute;inset:0;z-index:0;display:flex;align-items:center;justify-content:center;color:#F2EDE3;font-size:22px}
.avatar-wrap img{position:absolute;inset:0;z-index:1;width:100%;height:100%;object-fit:cover;display:block}
.name{font-size:15px;font-weight:700;color:#1C1C1E}.date{font-size:13px;color:#888;margin-top:2px}
.post-body{height:566px;flex:1;min-height:0;overflow:hidden}
.post-body p{font-size:18px;line-height:1.6;color:#333;margin-bottom:8px}
.post-body strong{color:#1C1C1E;font-weight:700}
.post-body .h1{font:800 27px/1.35 "Songti SC",serif;color:#1C1C1E;text-align:center;border-top:2px solid #1C1C1E;border-bottom:2px solid #1C1C1E;padding:16px 0;margin-bottom:24px}
.post-body .h2{font-size:22px;line-height:1.4;color:#1C1C1E;font-weight:700;border-left:4px solid #C4956A;padding-left:12px;margin-bottom:12px}
.post-body .h3{font-size:19px;line-height:1.4;color:#2C2A28;font-weight:700;margin:4px 0 10px}
.post-body .h4{font-size:19px;line-height:1.4;color:#2C2A28;font-weight:700;margin:4px 0 10px}
.list-item{display:flex;gap:8px;margin-bottom:7px;font-size:18px;line-height:1.6}.list-item .bullet{color:#999;font-weight:700;flex-shrink:0}.list-item.sub{margin-left:18px;font-size:16px}
code{background:#E8E0D1;color:#1C1C1E;padding:1px 5px;border-radius:4px;font-family:Menlo,monospace;font-size:.92em;white-space:nowrap}
code.cmd-block{display:block;white-space:pre-wrap;word-break:break-word;padding:8px 12px;line-height:1.6}
.code-block{background:#1C1C1E;color:#F2EDE3;border-radius:8px;padding:14px 16px;margin:8px 0 14px;font:14px/1.6 Menlo,monospace;white-space:pre-wrap;word-break:break-word}
a{color:inherit;text-decoration:underline;text-decoration-color:#999;text-underline-offset:3px}
.table-row{padding:6px 0;border-bottom:1px solid #999;font-size:15.5px;line-height:1.6}.table-row .key{font-size:16px;font-weight:700;color:#1C1C1E}
.post-footer{padding-top:10px;border-top:1px solid #d8d1c6;display:flex;justify-content:space-between;align-items:center;flex-shrink:0;height:30px;color:#888;font-size:12px}.gz{color:#C4956A;font-weight:700}
.swipe-hint{font-size:12px;color:#888;text-align:center;padding-bottom:8px}.cover .post-body{display:flex;flex-direction:column;justify-content:center}.quote-card{display:flex;flex-direction:column;justify-content:center;gap:26px}.quote-card .q{font-size:18px;font-weight:400;line-height:1.7;color:#2C2A28}.reading-note{font-size:12px;line-height:1.6;color:#888;margin-top:6px;padding-top:8px;border-top:1px solid #d8d1c6}
.cover .bg-paper,.closing .bg-paper{background:#1C1C1E}.cover .name,.closing .name{color:#F2EDE3}.cover .date,.closing .date{color:#aaa}.cover .post-body .h1{color:#F2EDE3;border-color:#C4956A}.cover .post-body p{color:#d8d1c6}.cover .swipe-hint{color:#aaa}.cover .post-footer,.closing .post-footer{color:#aaa;border-color:#444}.closing .quote-card .q,.closing .quote-card p{color:#F2EDE3}.closing .quote-card .q{padding-left:18px;border-left:3px solid #C4956A}
@media(max-width:570px){body{padding-left:0;padding-right:0}.slide{zoom:calc((100vw - 16px)/540px)}}
`;

function blocksFromMarkdown() {
  const blocks = [];
  let cursor = source.indexOf(markdown);
  const add = (token, html, kind, line, extra = {}) => blocks.push({ id: `block-${String(blocks.length + 1).padStart(3, '0')}`, kind, line, html, ...extra });
  for (const token of marked.lexer(markdown)) {
    const offset = source.indexOf(token.raw, cursor);
    const line = source.slice(0, offset).split('\n').length;
    cursor = offset + token.raw.length;
    if (['space', 'hr'].includes(token.type)) continue;
    if (token.type === 'heading') add(token, `<div class="h${token.depth}">${marked.parseInline(token.text)}</div>`, 'heading', line, { depth: token.depth });
    else if (token.type === 'paragraph') add(token, `<p>${marked.parseInline(token.text)}</p>`, 'paragraph', line);
    else if (token.type === 'blockquote') add(token, `<p>${marked.parseInline(token.text.replace(/\n/g, ' '))}</p>`, 'quote', line);
    else if (token.type === 'list') {
      let itemCursor = offset;
      token.items.forEach((item, index) => {
        const itemOffset = source.indexOf(item.raw, itemCursor);
        itemCursor = itemOffset + item.raw.length;
        const itemLine = source.slice(0, itemOffset).split('\n').length;
        const renderItems = (listItem, depth = 0) => {
          const textTokens = listItem.tokens.filter(part => part.type !== 'list' && part.type !== 'space');
          const inline = textTokens.map(part => marked.parseInline(part.text || '')).join('<br>');
          add(listItem, `<div class="list-item${depth ? ' sub' : ''}"><span class="bullet">${token.ordered ? `${token.start + index}.` : '•'}</span><div class="item-text">${inline}</div></div>`, 'list', itemLine);
          listItem.tokens.filter(part => part.type === 'list').forEach(list => list.items.forEach(child => renderItems(child, depth + 1)));
        };
        renderItems(item);
      });
    } else if (token.type === 'code') {
      const lines = token.text.split('\n');
      const visible = lines.slice(0, 8).join('\n');
      add(token, `<pre class="code-block">${escape(visible)}${lines.length > 8 ? '\n// 完整代码见公众号原文「墨筝」' : ''}</pre>`, 'code', line, { codeLines: lines.length, codeTruncated: lines.length > 8 });
    } else if (token.type === 'table') {
      token.rows.forEach(row => add(token, `<div class="table-row">${row.map((cell, index) => `<div><span class="key">${marked.parseInline(token.header[index].text)}：</span>${marked.parseInline(cell.text)}</div>`).join('')}</div>`, 'table', line));
    } else throw new Error(`Unsupported Markdown token: ${token.type} at ${line}`);
  }
  return blocks;
}

const downloadScript = `
const SCALE=2;
function flattenAlpha(canvas,bgColor){const flat=document.createElement('canvas');flat.width=canvas.width;flat.height=canvas.height;const context=flat.getContext('2d');context.fillStyle=bgColor||'#F2EDE3';context.fillRect(0,0,flat.width,flat.height);context.drawImage(canvas,0,0);return flat;}
async function inlineRemoteImages(){await Promise.all(Array.from(document.images).map(image=>image.decode()));}
async function renderSlide(slide){await document.fonts.ready;await inlineRemoteImages();const raw=await html2canvas(slide,{scale:SCALE,width:540,height:720,backgroundColor:null,useCORS:true,allowTaint:false,logging:false});return flattenAlpha(raw,'#F2EDE3');}
function canvasToBlob(canvas){return new Promise((resolve,reject)=>canvas.toBlob(blob=>blob?resolve(blob):reject(new Error('PNG 导出失败')),'image/png'));}
async function downloadAll(){const progress=document.getElementById('progress');try{const slides=Array.from(document.querySelectorAll('.slide'));const zip=new JSZip();for(let index=0;index<slides.length;index++){progress.textContent='渲染 '+(index+1)+' / '+slides.length;zip.file('Jev-'+String(index+1).padStart(2,'0')+'.png',await canvasToBlob(await renderSlide(slides[index])));}saveAs(await zip.generateAsync({type:'blob'}),'Jev-小红书素材.zip');progress.textContent=slides.length+' 张已打包下载';}catch(error){progress.textContent='下载失败：'+error.message;alert(progress.textContent);throw error;}}
async function downloadOne(){const progress=document.getElementById('progress');try{const index=Number(document.getElementById('current').value);saveAs(await canvasToBlob(await renderSlide(document.getElementById('slide-'+index))),'Jev-'+String(index).padStart(2,'0')+'.png');progress.textContent='第 '+index+' 张已下载';}catch(error){progress.textContent='下载失败：'+error.message;alert(progress.textContent);throw error;}}
`;

async function generate(page, blocks) {
  const avatar = `data:image/jpeg;base64,${fs.readFileSync(path.join(root, 'content/_shared/avatar.jpg')).toString('base64')}`;
  const header = `<div class="post-header"><div class="avatar-wrap"><span class="avatar-fallback">墨</span><img src="${avatar}" alt="墨筝" onerror="this.style.display='none'"></div><div><div class="name">墨筝</div><div class="date">${publishedLabel}</div></div></div>`;
  const footer = number => `<div class="post-footer"><div>微信搜索公众号<span class="gz">「墨筝」</span>查看更多内容</div><div class="page">${number} / TOTAL</div></div>`;
  const wrap = (body, number, type = '') => `<div class="slide ${type}" id="slide-${number}"><div class="bg-paper"></div><div class="content">${header}<div class="post-body ${type === 'closing' ? 'quote-card' : ''}">${body}</div>${type === 'cover' ? '<div class="swipe-hint">← 左滑查看更多</div>' : ''}${footer(number)}</div></div>`;
  await page.setContent(`<style>${css}</style>${wrap('', 1)}`);
  const result = await page.evaluate(input => {
    const body = document.querySelector('.post-body');
    const blocks = input.map(block => {
      const holder = document.createElement('div'); holder.innerHTML = block.html;
      holder.querySelectorAll('code').forEach(element => { if (element.textContent.length > 26) element.classList.add('cmd-block'); });
      block.html = holder.innerHTML;
      const content = holder.querySelector('.item-text') || holder.firstElementChild;
      const text = content.textContent;
      const fragments = [];
      const ends = [];
      if (['paragraph', 'quote', 'list'].includes(block.kind)) {
        for (const match of text.matchAll(/[。！？](?:[”’」』）)]*)/g)) ends.push(match.index + match[0].length);
      }
      if (ends.at(-1) !== text.length) ends.push(text.length);
      let start = 0;
      const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT);
      const nodes = []; let current; let offset = 0;
      while ((current = walker.nextNode())) { nodes.push({ node: current, start: offset, end: offset + current.length }); offset += current.length; }
      for (const end of ends) {
        if (!nodes.length) continue;
        const first = nodes.find(entry => entry.end > start) || nodes.at(-1);
        const last = nodes.find(entry => entry.end >= end) || nodes.at(-1);
        const range = document.createRange(); range.setStart(first.node, start - first.start); range.setEnd(last.node, end - last.start);
        const piece = document.createElement('div'); piece.append(range.cloneContents());
        fragments.push({ start, end, html: piece.innerHTML }); start = end;
      }
      return { ...block, text, fragments };
    });
    const contentBlocks = blocks.slice(1);
    const slides = []; let placed = [];
    const render = entries => entries.map(entry => {
      const block = blocks.find(candidate => candidate.id === entry.id);
      const holder = document.createElement('div'); holder.innerHTML = block.html;
      const target = holder.querySelector('.item-text') || holder.firstElementChild;
      target.innerHTML = entry.html;
      holder.firstElementChild.dataset.sourceBlock = entry.id;
      holder.firstElementChild.dataset.start = entry.start;
      holder.firstElementChild.dataset.end = entry.end;
      return holder.innerHTML;
    }).join('');
    const fits = (entries, reserve = 0) => {
      body.innerHTML = render(entries);
      const bottom = body.lastElementChild?.getBoundingClientRect().bottom || body.getBoundingClientRect().top;
      return bottom <= body.getBoundingClientRect().bottom - reserve && Array.from(body.querySelectorAll('*')).every(element => element.scrollWidth <= element.clientWidth + 1);
    };
    const append = (entries, block, fragment) => {
      const next = entries.map(entry => ({ ...entry }));
      if (next.at(-1)?.id === block.id) { next.at(-1).html += fragment.html; next.at(-1).end = fragment.end; }
      else next.push({ id: block.id, ...fragment });
      return next;
    };
    let stopped = false;
    for (let blockIndex = 0; blockIndex < contentBlocks.length && !stopped; blockIndex++) {
      const block = contentBlocks[blockIndex];
      for (const fragment of block.fragments) {
        let next = append(placed, block, fragment);
        let check = next;
        if (block.kind === 'heading') {
          let followingIndex = blockIndex + 1;
          while (contentBlocks[followingIndex]?.kind === 'heading') {
            check = append(check, contentBlocks[followingIndex], contentBlocks[followingIndex].fragments[0]); followingIndex++;
          }
          if (contentBlocks[followingIndex]) check = append(check, contentBlocks[followingIndex], contentBlocks[followingIndex].fragments[0]);
        }
        const reserve = slides.length === 15 ? 52 : 0;
        if (!fits(check, reserve)) {
          if (!placed.length) throw new Error('A source sentence exceeds one card: '+block.id);
          slides.push({ entries: placed, html: render(placed) }); placed = [];
          if (slides.length === 16) { stopped = true; break; }
          next = append(placed, block, fragment);
          if (!fits(next, slides.length === 15 ? 52 : 0)) throw new Error('Cannot fit source fragment '+block.id+' line '+block.line+': '+block.html);
        }
        placed = next;
      }
    }
    if (placed.length) slides.push({ entries: placed, html: render(placed) });
    return { blocks, slides, truncated: stopped };
  }, blocks);
  const opening = blocks[0].html.replace('<p>', '<p data-source-block="block-001" data-start="0" data-end="'+result.blocks[0].text.length+'">');
  const cards = [wrap(`<div class="h1">${escape(title)}</div>${opening}`, 1, 'cover')];
  result.slides.forEach((slide, index) => cards.push(wrap(slide.html + (result.truncated && index === result.slides.length - 1 ? '<div class="reading-note">完整内容请移步微信公众号「墨筝」阅读原文</div>' : ''), index + 2)));
  const quote = '把判断与生成清晰解耦，系统往往能变得更简单、更可靠。';
  assert(result.blocks.some(block => block.text.includes(quote)));
  cards.push(wrap(`<div class="q">${quote}</div><p>微信搜索公众号「墨筝」<br>阅读《关于 Jev, 看这篇就够了》完整原文</p>`, cards.length + 1, 'closing'));
  const dependencies = [
    ['html2canvas', 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js'],
    ['jszip', 'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js'],
    ['file-saver', 'https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js']
  ].map(([name, url]) => {
    const cache = path.join(out, `.xhs-${name}.js`);
    if (!fs.existsSync(cache)) fs.writeFileSync(cache, execFileSync('curl', ['--fail', '--location', '--silent', '--show-error', url], { maxBuffer: 3e6 }));
    return `<script>${fs.readFileSync(cache, 'utf8').replaceAll('</script', '<\\/script')}</script>`;
  }).join('\n');
  const html = `<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)}</title><style>${css}</style></head><body><div class="toolbar"><button onclick="downloadAll()">全部下载 (ZIP)</button><select id="current" aria-label="当前卡片">${cards.map((_, index) => `<option value="${index + 1}">第 ${index + 1} 张</option>`).join('')}</select><button onclick="downloadOne()">下载当前</button><a href="xiaohongshu/Jev-小红书素材.zip" download>已导出 ZIP</a><span id="progress"></span></div>${cards.join('\n').replaceAll('TOTAL', String(cards.length))}${dependencies}<script>${downloadScript}</script></body></html>`;
  fs.writeFileSync(htmlPath, html);
  const mapping = result.blocks.map(block => {
    const ranges = block.id === 'block-001' ? [{ slide: 1, start: 0, end: block.text.length }] : result.slides.flatMap((slide, index) => slide.entries.filter(entry => entry.id === block.id).map(entry => ({ slide: index + 2, start: entry.start, end: entry.end })));
    const covered = ranges.at(-1)?.end || 0;
    return { id: block.id, kind: block.kind, depth: block.depth, source_line: block.line, original_text: block.text, ranges, status: covered === block.text.length ? 'complete' : covered ? 'partial' : 'not_reached' };
  });
  const last = mapping.filter(block => block.ranges.length).at(-1);
  const report = { source: 'source/_posts/about-jev.md', title, card_count: cards.length, truncated: result.truncated, last_source_block: last.id, last_source_line: last.source_line, last_sentence: last.original_text.slice(0, last.ranges.at(-1).end).match(/[^。！？]*[。！？][”’」』）)]*$/)?.[0] || last.original_text, coverage: mapping };
  fs.writeFileSync(path.join(out, 'xiaohongshu-source-map.json'), JSON.stringify(report, null, 2));
  return report;
}

async function validateAndExport(page, report) {
  await page.goto(require('node:url').pathToFileURL(htmlPath).href);
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all(Array.from(document.images).map(image => image.decode())); });
  const geometry = await page.evaluate(() => Array.from(document.querySelectorAll('.slide')).map(slide => {
    const body = slide.querySelector('.post-body'); const footer = slide.querySelector('.post-footer'); const bounds = body.getBoundingClientRect();
    const children = Array.from(body.children).map(element => ({ tag: element.className || element.tagName, top: element.getBoundingClientRect().top, bottom: element.getBoundingClientRect().bottom }));
    return { slide: slide.id, height: body.clientHeight, scroll: body.scrollHeight, used: children.length ? children.at(-1).bottom - children[0].top : 0, overflow: body.scrollHeight > body.clientHeight + 1 || children.some(child => child.bottom > bounds.bottom + 1) || bounds.bottom > footer.getBoundingClientRect().top + 1, horizontal: Array.from(body.querySelectorAll('*')).some(element => element.scrollWidth > element.clientWidth + 1), fragments: Array.from(body.querySelectorAll('[data-source-block]')).map(element => ({ id: element.dataset.sourceBlock, start: Number(element.dataset.start), end: Number(element.dataset.end), text: (element.querySelector('.item-text') || element).textContent })) };
  }));
  assert.equal(geometry.length, report.card_count);
  for (const slide of geometry) {
    assert(!slide.overflow && !slide.horizontal, `Overflow: ${JSON.stringify(slide)}`);
    for (const fragment of slide.fragments) {
      const block = report.coverage.find(candidate => candidate.id === fragment.id);
      assert.equal(fragment.text, block.original_text.slice(fragment.start, fragment.end), `Text mismatch: ${fragment.id}`);
    }
  }
  for (const block of report.coverage.filter(block => block.ranges.length)) {
    let cursor = 0;
    for (const range of block.ranges) { assert.equal(range.start, cursor, `Source gap ${block.id}`); cursor = range.end; }
  }
  const firstNotReached = report.coverage.findIndex(block => block.status !== 'complete');
  if (firstNotReached >= 0) assert(report.coverage.slice(firstNotReached + 1).every(block => block.status === 'not_reached'));
  for (const slide of geometry.slice(1, -1)) assert(slide.used >= 283, `Sparse card: ${slide.slide}`);
  const headings = await page.locator('.h2,.h3').allTextContents();
  headings.forEach(heading => assert(source.split('\n').some(line => line === `## ${heading}` || line === `### ${heading}`), `Invented heading ${heading}`));
  const colors = await page.evaluate(() => {
    const selectors = { strong: '.post-body strong', h3: '.post-body .h3', bullet: '.list-item .bullet', code: '.post-body code', paper: '.slide:not(.cover):not(.closing) .bg-paper' };
    return Object.fromEntries(Object.entries(selectors).map(([name, selector]) => [name, Array.from(new Set(Array.from(document.querySelectorAll(selector)).map(element => getComputedStyle(element)[name === 'paper' ? 'backgroundColor' : 'color'])))]));
  });
  assert.deepEqual(colors.strong, ['rgb(28, 28, 30)']); assert.deepEqual(colors.h3, ['rgb(44, 42, 40)']); assert.deepEqual(colors.bullet, ['rgb(153, 153, 153)']); assert.deepEqual(colors.code, ['rgb(28, 28, 30)']); assert.deepEqual(colors.paper, ['rgb(242, 237, 227)']);
  fs.mkdirSync(imageDir, { recursive: true });
  const pngs = [];
  for (let index = 1; index <= report.card_count; index++) {
    const base64 = await page.evaluate(async number => (await renderSlide(document.getElementById('slide-'+number))).toDataURL('image/png').split(',')[1], index);
    const png = Buffer.from(base64, 'base64'); assert.equal(png.readUInt32BE(16), 1080); assert.equal(png.readUInt32BE(20), 1440);
    const filename = `Jev-${String(index).padStart(2, '0')}.png`; fs.writeFileSync(path.join(imageDir, filename), png); pngs.push({ filename, base64 });
    console.log(`PNG ${index}/${report.card_count}: 1080x1440`);
  }
  const zipData = await page.evaluate(async pngs => { const zip = new JSZip(); pngs.forEach(png => zip.file(png.filename, png.base64, { base64: true })); return zip.generateAsync({ type: 'base64', compression: 'DEFLATE' }); }, pngs);
  fs.writeFileSync(path.join(imageDir, 'Jev-小红书素材.zip'), Buffer.from(zipData, 'base64'));
  for (const number of [1, 5, report.card_count]) await page.locator(`#slide-${number}`).screenshot({ path: path.join(out, `xiaohongshu-check-${number}.png`) });
  const download = page.waitForEvent('download'); await page.locator('button', { hasText: '下载当前' }).click(); const downloaded = await download; assert.equal(downloaded.suggestedFilename(), 'Jev-01.png');
  const zipDownload = page.waitForEvent('download'); await page.locator('a', { hasText: '已导出 ZIP' }).click(); assert.equal((await zipDownload).suggestedFilename(), 'Jev-小红书素材.zip');
  await page.setViewportSize({ width: 390, height: 844 });
  assert(await page.locator('#slide-1').evaluate(element => element.getBoundingClientRect().width <= 390));
  fs.writeFileSync(path.join(out, 'xiaohongshu-validation.json'), JSON.stringify({ passed: true, colors, geometry, png_count: pngs.length, dimensions: [1080, 1440], current_download: 'passed', local_zip_download: 'passed', mobile: 'passed' }, null, 2));
}

async function main() {
  const tokens = marked.lexer(markdown);
  assert.equal(tokens.find(token => token.type === 'heading').text, 'Jev 到底是什么？');
  assert.equal(tokens.some(token => token.type === 'image'), false);
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  const page = await browser.newPage();
  await page.setContent('<p style="font-size:18px;line-height:1.6">Jev</p>');
  assert.equal(await page.locator('p').evaluate(element => getComputedStyle(element).fontSize), '18px');
  const immutable = ['source/_posts/about-jev.md', 'content/about-jev/preview.html'].map(filename => [filename, fs.readFileSync(path.join(root, filename))]);
  const manifestPath = path.join(out, 'manifest.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath));
  const wechatBefore = JSON.stringify(manifest.outputs.wechat);
  try {
    await page.setViewportSize({ width: 1200, height: 900 });
    const report = await generate(page, blocksFromMarkdown());
    await validateAndExport(page, report);
    const copy = { title: 'Jev拆解｜不写文本的AI决策模型', body: '一个 AI 模型，网络里甚至没有生成字符串的路径。Jev 不负责写答案，只负责给业务代码返回选择、评分和概率。\n\n这篇长文把它拆成了一本工程账：为什么逐字生成会变成“语言税”，官方的 193 倍速度和 444 倍成本优势该怎么理解，以及单次调用很便宜，为什么高频循环仍可能每月烧掉 5000 美元。\n\n真正值得关注的不是宣传数字，而是概率校准、弃权机制和每次可接受决策的综合成本。轮播按原文顺序展开，完整技术边界、架构范式与 TypeScript 实战见公众号「墨筝」。', tags: ['AI', 'Jev', 'AI工程', 'Agent', '模型选型', '结构化输出', '软件架构', 'TypeScript', '人工智能', '开发者'] };
    assert(Array.from(copy.title).length <= 20); assert(Array.from(copy.body).length >= 150 && Array.from(copy.body).length <= 250); assert(copy.tags.length >= 8 && copy.tags.length <= 12);
    fs.writeFileSync(path.join(out, 'xiaohongshu-copy.md'), `# 小红书发布文案\n\n标题：${copy.title}\n\n${copy.body}\n\n.\n${copy.tags.map(tag => '#'+tag).join(' ')}\n`);
    manifest.outputs.xiaohongshu = { html: 'content/about-jev/Jev-小红书版.html', images_dir: 'content/about-jev/xiaohongshu', copy };
    assert.equal(JSON.stringify(manifest.outputs.wechat), wechatBefore);
    fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2)+'\n');
    immutable.forEach(([filename, content]) => assert(fs.readFileSync(path.join(root, filename)).equals(content)));
    console.log(JSON.stringify({ cards: report.card_count, last_source_line: report.last_source_line, last_sentence: report.last_sentence, copy_length: Array.from(copy.body).length, wechat: 'unchanged', source_and_preview: 'unchanged' }, null, 2));
  } finally { await browser.close(); }
}

main().catch(error => { console.error(error); process.exitCode = 1; });