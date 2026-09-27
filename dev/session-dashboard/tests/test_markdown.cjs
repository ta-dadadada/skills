const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {test} = require('node:test');

// ブラウザに依存せず、出力とクリップボードの失敗経路を検証する。
function element(tag, children = [], dataset = {}) {
  children = children.map(child => typeof child === 'string'
    ? {nodeType: 3, textContent: child} : child);
  return {
    nodeType: 1, tagName: tag.toUpperCase(), childNodes: children, dataset,
    get children() { return children.filter(child => child.nodeType === 1); },
    get textContent() { return children.map(child => child.textContent).join(''); },
    querySelectorAll(selector) {
      return this.children.flatMap(child => [
        ...(child.tagName.toLowerCase() === selector ? [child] : []),
        ...child.querySelectorAll(selector),
      ]);
    },
    querySelector(selector) { return this.querySelectorAll(selector)[0]; },
    cloneNode() { return element(tag, children, dataset); },
  };
}
function setup(clipboard) {
  const controls = Object.fromEntries(['copy-markdown', 'copy-status', 'copy-fallback', 'markdown-text', 'close-copy'].map(id => [id, {
    hidden: true, disabled: false,
    addEventListener(event, fn) { this[event] = fn; },
    focus() { this.focused = true; }, select() { this.selected = true; },
  }]));
  let main = element('main', [element('h1', ['目的']), element('p', ['初回'])]);
  const context = vm.createContext({
    Node: {TEXT_NODE: 3, ELEMENT_NODE: 1}, navigator: {clipboard},
    location: {protocol: 'file:'},
    document: {getElementById: id => controls[id], querySelector: () => main},
  });
  const html = fs.readFileSync(path.join(__dirname, '../assets/dashboard.html'), 'utf8');
  vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1], context);
  return {controls, context, setMain: value => { main = value; }};
}

test('Markdown preserves literal punctuation, sections and TODO states', () => {
  const {context} = setup();
  const output = context.dashboardMarkdown(element('main', [
    element('h1', ['目的']), element('p', ['&copy;\n---\n[link](url) <tag> C:\\work']),
    element('ul', [element('li', ['完了'], {todoStatus: 'done'}), element('li', ['作業中'], {todoStatus: 'in_progress'})]),
    element('dl', [element('div', [element('dt', ['モデル']), element('dd', ['unknown']), element('p', ['未取得'])])]),
  ]));
  assert.ok(output.startsWith('# 目的\n\n'));
  assert.ok(output.includes('\\&copy\\;\n\\-\\-\\-'));
  assert.ok(output.includes('\\[link\\]\\(url\\) \\<tag\\> C\\:\\\\work'));
  assert.ok(output.includes('- [x] 完了\n- [ ] 作業中'));
  assert.ok(output.includes('- **モデル**: unknown (未取得)'));
});

test('success copies the latest document without fallback', async () => {
  let copied;
  const app = setup({writeText: async text => { copied = text; }});
  app.setMain(element('main', [element('h1', ['更新後']), element('p', ['最新内容'])]));
  await app.controls['copy-markdown'].click();
  assert.equal(copied, '# 更新後\n\n最新内容\n');
  assert.equal(app.controls['copy-fallback'].hidden, true);
  assert.equal(app.controls['copy-status'].textContent, 'Markdownをコピーしました。');
  assert.equal(app.controls['copy-markdown'].disabled, false);
});

for (const clipboard of [undefined, {writeText: async () => { throw new Error('denied'); }}]) {
  test(`clipboard ${clipboard ? 'denied' : 'missing'} keeps selectable snapshot and returns focus`, async () => {
    const app = setup(clipboard);
    await app.controls['copy-markdown'].click();
    const field = app.controls['markdown-text'];
    assert.equal(app.controls['copy-fallback'].hidden, false);
    assert.equal(field.focused, true);
    assert.equal(field.selected, true);
    assert.equal(field.value, '# 目的\n\n初回\n');
    app.setMain(element('main', ['変更後']));
    assert.equal(field.value, '# 目的\n\n初回\n');
    app.controls['close-copy'].click();
    assert.equal(app.controls['copy-fallback'].hidden, true);
    assert.equal(app.controls['copy-markdown'].focused, true);
    assert.equal(app.controls['copy-markdown'].disabled, false);
  });
}
