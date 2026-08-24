"""HTTPから独立したHTMLレンダリング。"""

from __future__ import annotations

import html
from string import Template

from .spec import MAX_ROUNDS, FormSpec, Question
from .submission import OTHER_VALUE


VOID_ELEMENTS = {"input", "meta", "br"}


def text(value: object) -> str:
    return html.escape(str(value), quote=False)


def el(tag: str, attrs: dict[str, object] | None = None, *children: str) -> str:
    """エスケープ済み属性と子要素から小さなHTML断片を作る。"""

    parts: list[str] = []
    for key, value in (attrs or {}).items():
        if value is None or value is False:
            continue
        if value is True:
            parts.append(f" {key}")
        else:
            escaped = html.escape(str(value), quote=True)
            parts.append(f' {key}="{escaped}"')
    open_tag = f"<{tag}{''.join(parts)}>"
    if tag in VOID_ELEMENTS:
        return open_tag
    return f"{open_tag}{''.join(children)}</{tag}>"


CSS = """
:root {
  --canvas: #edf3f8;
  --paper: #ffffff;
  --ink: #172033;
  --muted: #5d697b;
  --line: #cbd7e3;
  --action: #315cf4;
  --complete: #0e7c7b;
  --danger: #b54708;
  --shadow: 0 18px 48px rgba(31, 54, 84, .12);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--canvas);
  color: var(--ink);
  font-family: Inter, "Hiragino Sans", "Yu Gothic UI", system-ui, sans-serif;
  line-height: 1.6;
}
button, input, textarea { font: inherit; }
.shell { display: grid; grid-template-columns: 280px minmax(0, 780px); gap: 40px; max-width: 1160px; margin: 0 auto; padding: 48px 28px 96px; }
.rail { position: sticky; top: 24px; align-self: start; padding: 24px; background: #14233d; color: white; border-radius: 18px; box-shadow: var(--shadow); }
.rail-kicker, .eyebrow { margin: 0 0 6px; font: 700 .72rem/1.2 ui-monospace, "SFMono-Regular", monospace; letter-spacing: .13em; text-transform: uppercase; }
.rail-kicker { color: #9fb5ff; }
.rail h2 { margin: 0; font: 650 1.25rem/1.25 "Avenir Next", "Hiragino Sans", system-ui, sans-serif; }
.overall { margin: 24px 0 22px; }
.overall-copy { display: flex; justify-content: space-between; gap: 12px; color: #c8d4e8; font-size: .82rem; }
.track { height: 7px; margin-top: 9px; overflow: hidden; border-radius: 99px; background: #30415f; }
.track span { display: block; width: 0; height: 100%; background: #64d1c8; transition: width .2s ease; }
.rail-nav { display: grid; gap: 4px; }
.rail-link { display: grid; grid-template-columns: 30px 1fr; gap: 9px; padding: 10px 8px; border-radius: 10px; color: #e9eef8; text-decoration: none; }
.rail-link:hover, .rail-link:focus-visible { background: #223553; outline: none; }
.rail-link.complete { color: #8be0d8; }
.rail-index { font: 700 .72rem/1.8 ui-monospace, "SFMono-Regular", monospace; color: #9fb5ff; }
.rail-copy { display: flex; justify-content: space-between; gap: 8px; align-items: baseline; }
.rail-copy strong { font-size: .88rem; }
.rail-copy small { color: #aebbd0; white-space: nowrap; }
.stage { min-width: 0; }
.hero { padding: 10px 4px 30px; }
.eyebrow { color: var(--action); }
.hero h1 { margin: 0; max-width: 22ch; font: 650 clamp(2.1rem, 4.5vw, 3.35rem)/1.04 "Avenir Next", "Hiragino Sans", system-ui, sans-serif; letter-spacing: -.04em; text-wrap: balance; }
.intro { max-width: 65ch; margin: 18px 0 0; color: var(--muted); font-size: 1.04rem; }
.form-context { margin: 0 0 24px; padding: 20px 22px; border: 1px solid #b8cae4; border-left: 5px solid var(--action); border-radius: 14px; background: #f7faff; }
.form-context h2, .context-kicker { margin: 0; color: #2949bd; font: 800 .72rem/1.3 ui-monospace, "SFMono-Regular", monospace; letter-spacing: .08em; text-transform: uppercase; }
.form-context p { margin: 9px 0 0; max-width: 70ch; white-space: pre-wrap; }
.draft { margin: 0 0 24px; overflow: hidden; border: 1px solid #a9b9ca; border-radius: 16px; background: #e3ebf4; }
.draft summary { cursor: pointer; padding: 14px 18px; font-weight: 700; }
.draft pre { margin: 0; padding: 0 18px 18px; white-space: pre-wrap; font: .88rem/1.65 ui-monospace, "SFMono-Regular", monospace; }
.form-section { margin-bottom: 22px; padding: 28px; border: 1px solid var(--line); border-radius: 18px; background: var(--paper); box-shadow: 0 8px 28px rgba(31, 54, 84, .06); scroll-margin-top: 24px; }
.form-section > header { display: grid; grid-template-columns: 40px 1fr; gap: 12px; margin-bottom: 12px; }
.section-number { padding-top: 3px; color: var(--action); font: 800 .77rem/1.5 ui-monospace, "SFMono-Regular", monospace; }
.form-section h2 { margin: 0; font: 650 1.38rem/1.25 "Avenir Next", "Hiragino Sans", system-ui, sans-serif; }
.section-description { margin: 5px 0 0; color: var(--muted); }
.question { min-width: 0; margin: 0; padding: 24px 0; border: 0; border-top: 1px solid #e5ebf1; }
.question-context { margin: 0 0 14px; padding: 12px 14px; border-left: 3px solid #8ca8d9; border-radius: 0 9px 9px 0; background: #f4f7fc; }
.question-context .context-kicker { color: #425f91; }
.context-copy { margin: 5px 0 0; color: #35445a; font-size: .91rem; white-space: pre-wrap; }
.question-group { min-width: 0; margin: 0; padding: 0; border: 0; }
.question-heading { display: flex; width: 100%; justify-content: space-between; gap: 18px; align-items: flex-start; padding: 0; }
.question-label { font-weight: 700; line-height: 1.45; }
.requirement { flex: none; padding: 2px 8px; border-radius: 99px; background: #e9eefc; color: #2949bd; font-size: .7rem; font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
.question[data-required="false"] .requirement { background: #edf0f3; color: #4f5967; }
.question-help { margin: 7px 0 13px; color: var(--muted); font-size: .9rem; }
input[type="text"], textarea { width: 100%; border: 1px solid #aebdcb; border-radius: 10px; background: #fbfdff; color: var(--ink); padding: 12px 13px; }
textarea { resize: vertical; min-height: 132px; }
input[type="text"]:focus, textarea:focus { border-color: var(--action); outline: 3px solid rgba(49, 92, 244, .18); }
.choices { display: grid; gap: 9px; }
.choice { display: flex; align-items: flex-start; gap: 10px; padding: 11px 12px; border: 1px solid #c7d2dd; border-radius: 10px; cursor: pointer; background: #fbfdff; }
.choice:hover { border-color: #8297ad; }
.choice:has(input:checked) { border-color: var(--action); background: #f0f3ff; }
.choice input[type="radio"], .choice input[type="checkbox"] { width: 18px; height: 18px; margin-top: 3px; accent-color: var(--action); }
.choice-other { flex-wrap: wrap; cursor: default; }
.choice-select { display: flex; align-items: flex-start; gap: 10px; cursor: pointer; }
.other-input { flex: 1 1 220px; padding: 7px 9px !important; }
.field-error { display: none; margin: 8px 0 0; color: var(--danger); font-size: .86rem; font-weight: 700; }
.question.invalid { margin-inline: -12px; padding-inline: 12px; border-radius: 10px; background: #fff5ec; }
.question.invalid .field-error { display: block; }
.actions { display: flex; justify-content: flex-end; align-items: center; gap: 16px; margin-top: 28px; padding: 14px; border: 1px solid var(--line); border-radius: 16px; background: var(--paper); box-shadow: var(--shadow); }
.form-error { flex: 1; margin: 0; color: var(--danger); font-weight: 700; }
.save { min-width: 170px; border: 0; border-radius: 10px; background: var(--action); color: white; padding: 12px 20px; font-weight: 800; cursor: pointer; }
.save:hover { background: #2448cf; }
.save:focus-visible { outline: 3px solid rgba(49, 92, 244, .3); outline-offset: 3px; }
.save:disabled { cursor: wait; opacity: .65; }
@media (max-width: 840px) {
  .shell { grid-template-columns: 1fr; padding: 24px 16px 72px; }
  .rail { position: static; }
  .rail-nav { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }
  .hero h1 { max-width: none; }
}
@media (max-width: 520px) {
  .form-section { padding: 20px 16px; }
  .question-heading { display: grid; gap: 8px; }
  .requirement { justify-self: start; }
  .actions { align-items: stretch; flex-direction: column; }
  .save { width: 100%; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .track span { transition: none; }
}
"""


SCRIPT = """
const form = document.getElementById('intake-form');
const cards = Array.from(document.querySelectorAll('.question'));
const validationMessage = form.dataset.validationMessage;

function answerState(card) {
  const type = card.dataset.type;
  if (type === 'short_text' || type === 'long_text') {
    return card.querySelector('input[type="text"], textarea').value.trim().length > 0;
  }
  const selected = Array.from(card.querySelectorAll('input[type="radio"]:checked, input[type="checkbox"]:checked'));
  if (!selected.length) return false;
  const other = selected.find(input => input.hasAttribute('data-other'));
  if (!other) return true;
  return card.querySelector('.other-input').value.trim().length > 0;
}

function refreshProgress() {
  let totalDone = 0;
  document.querySelectorAll('.form-section').forEach(section => {
    const sectionCards = Array.from(section.querySelectorAll('.question'));
    const done = sectionCards.filter(answerState).length;
    totalDone += done;
    const rail = document.querySelector('[data-rail="' + section.dataset.section + '"]');
    rail.querySelector('[data-done]').textContent = done;
    rail.classList.toggle('complete', done === sectionCards.length);
  });
  document.getElementById('answered-count').textContent = totalDone;
  document.getElementById('progress-bar').style.width = ((totalDone / cards.length) * 100) + '%';
}

form.addEventListener('input', refreshProgress);
form.addEventListener('change', refreshProgress);
form.addEventListener('submit', event => {
  const invalid = cards.filter(card =>
    (card.dataset.required === 'true' && !answerState(card)) ||
    (card.querySelector('[data-other]:checked') && !answerState(card))
  );
  cards.forEach(card => {
    card.classList.remove('invalid');
    card.querySelector('.field-error').textContent = '';
  });
  if (invalid.length) {
    event.preventDefault();
    invalid.forEach(card => {
      card.classList.add('invalid');
      card.querySelector('.field-error').textContent = validationMessage;
    });
    document.getElementById('form-error').textContent = validationMessage;
    invalid[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
    const focusable = invalid[0].querySelector('input, textarea');
    if (focusable) focusable.focus({ preventScroll: true });
    return;
  }
  document.getElementById('form-error').textContent = '';
  const button = form.querySelector('.save');
  button.disabled = true;
  button.textContent = form.dataset.savingLabel;
});
refreshProgress();
"""


PAGE_TEMPLATE = Template("""<!doctype html>
<html lang="$language">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<style>$css</style>
</head>
<body>
<main class="shell">
  <aside class="rail" aria-label="$progress_label">
    <p class="rail-kicker">$app_label</p>
    <h2>$progress_label</h2>
    <div class="overall">
      <div class="overall-copy"><span>$progress_label</span><strong><span id="answered-count">0</span> / $total_questions</strong></div>
      <div class="track" aria-hidden="true"><span id="progress-bar"></span></div>
    </div>
    <nav class="rail-nav">$nav_items</nav>
  </aside>
  <div class="stage">
    <header class="hero">
      <p class="eyebrow">$round_label $round_number / $max_rounds</p>
      <h1>$title</h1>
      <p class="intro">$intro</p>
    </header>
    $context
    $draft
    $form
  </div>
</main>
<script>$script</script>
</body>
</html>""")


MESSAGE_CSS = """
body { margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 24px; background: #edf3f8; color: #172033; font-family: Inter, "Hiragino Sans", system-ui, sans-serif; }
main { max-width: 560px; padding: 36px; border: 1px solid #cbd7e3; border-top: 7px solid #b54708; border-radius: 18px; background: white; box-shadow: 0 18px 48px rgba(31,54,84,.12); }
main.success { border-top-color: #0e7c7b; }
p { color: #5d697b; }
"""


MESSAGE_TEMPLATE = Template("""<!doctype html>
<html lang="$language"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title><style>$css</style></head>
<body><main class="$status_class"><h1>$title</h1><p>$message</p></main></body></html>""")


def _requirement(spec: FormSpec, question: Question) -> str:
    label = spec.ui.required_label if question.required else spec.ui.optional_label
    return el("span", {"class": "requirement"}, text(label))


def _question_context(spec: FormSpec, question: Question) -> str:
    if not question.context:
        return ""
    return el(
        "aside",
        {"class": "question-context", "id": f"{question.id}-context"},
        el("p", {"class": "context-kicker"}, text(spec.ui.context_label)),
        el("p", {"class": "context-copy"}, text(question.context)),
    )


def _described_by(question: Question) -> str | None:
    ids = []
    if question.context:
        ids.append(f"{question.id}-context")
    if question.help:
        ids.append(f"{question.id}-help")
    return " ".join(ids) or None


def _text_question(spec: FormSpec, question: Question) -> str:
    help_id = f"{question.id}-help"
    heading = el(
        "div",
        {"class": "question-heading"},
        el("label", {"class": "question-label", "for": question.id}, text(question.prompt)),
        _requirement(spec, question),
    )
    help_text = el("p", {"class": "question-help", "id": help_id}, text(question.help)) if question.help else ""
    common_attrs = {
        "id": question.id,
        "name": question.id,
        "placeholder": question.placeholder or None,
        "aria-describedby": _described_by(question),
        "required": question.required,
    }
    if question.type == "short_text":
        field = el("input", {"type": "text", **common_attrs})
    else:
        field = el("textarea", {**common_attrs, "rows": "6"})
    error = el("p", {"class": "field-error", "aria-live": "polite"})
    return el(
        "div",
        {
            "class": "question",
            "id": f"question-{question.id}",
            "data-question": question.id,
            "data-type": question.type,
            "data-required": str(question.required).lower(),
        },
        _question_context(spec, question),
        heading,
        help_text,
        field,
        error,
    )


def _choice(spec: FormSpec, question: Question, value: str, index: int) -> str:
    input_type = "radio" if question.type == "single_choice" else "checkbox"
    option_id = f"{question.id}-{index}"
    control = el(
        "input",
        {
            "type": input_type,
            "id": option_id,
            "name": question.id,
            "value": value,
            "required": question.required and input_type == "radio",
        },
    )
    return el("label", {"class": "choice", "for": option_id}, control, el("span", None, text(value)))


def _other_choice(spec: FormSpec, question: Question, index: int) -> str:
    input_type = "radio" if question.type == "single_choice" else "checkbox"
    option_id = f"{question.id}-{index}"
    control = el(
        "input",
        {
            "type": input_type,
            "id": option_id,
            "name": question.id,
            "value": OTHER_VALUE,
            "data-other": True,
            "required": question.required and input_type == "radio",
        },
    )
    other_text = el(
        "input",
        {
            "class": "other-input",
            "type": "text",
            "name": f"{question.id}__other_text",
            "aria-label": spec.ui.other_label,
        },
    )
    select_label = el(
        "label",
        {"class": "choice-select", "for": option_id},
        control,
        el("span", None, text(spec.ui.other_label)),
    )
    return el("div", {"class": "choice choice-other"}, select_label, other_text)


def _choice_question(spec: FormSpec, question: Question) -> str:
    help_id = f"{question.id}-help"
    legend = el(
        "legend",
        {"class": "question-heading"},
        el("span", {"class": "question-label"}, text(question.prompt)),
        _requirement(spec, question),
    )
    help_text = el("p", {"class": "question-help", "id": help_id}, text(question.help)) if question.help else ""
    choices = [_choice(spec, question, option, index) for index, option in enumerate(question.options)]
    if question.allow_other:
        choices.append(_other_choice(spec, question, len(question.options)))
    group = el("div", {"class": "choices"}, *choices)
    group_fieldset = el(
        "fieldset",
        {
            "class": "question-group",
            "aria-describedby": _described_by(question),
        },
        legend,
        help_text,
        group,
    )
    error = el("p", {"class": "field-error", "aria-live": "polite"})
    return el(
        "div",
        {
            "class": "question",
            "id": f"question-{question.id}",
            "data-question": question.id,
            "data-type": question.type,
            "data-required": str(question.required).lower(),
        },
        _question_context(spec, question),
        group_fieldset,
        error,
    )


def _question(spec: FormSpec, question: Question) -> str:
    if question.type in {"short_text", "long_text"}:
        return _text_question(spec, question)
    return _choice_question(spec, question)


def render_form(spec: FormSpec) -> bytes:
    """フォーム画面を静的CSS/JSと型付きデータから生成する。"""

    nav_items: list[str] = []
    section_cards: list[str] = []
    total_questions = 0
    for index, section in enumerate(spec.sections):
        count = len(section.questions)
        total_questions += count
        nav_items.append(
            el(
                "a",
                {"class": "rail-link", "href": f"#section-{section.id}", "data-rail": section.id},
                el("span", {"class": "rail-index"}, f"{index + 1:02d}"),
                el(
                    "span",
                    {"class": "rail-copy"},
                    el("strong", None, text(section.title)),
                    el("small", None, el("span", {"data-done": True}, "0"), f" / {count}"),
                ),
            )
        )
        description = (
            el("p", {"class": "section-description"}, text(section.description))
            if section.description
            else ""
        )
        section_header = el(
            "header",
            None,
            el("span", {"class": "section-number"}, f"{index + 1:02d}"),
            el("div", None, el("h2", None, text(section.title)), description),
        )
        section_cards.append(
            el(
                "section",
                {"class": "form-section", "id": f"section-{section.id}", "data-section": section.id},
                section_header,
                *[_question(spec, question) for question in section.questions],
            )
        )

    draft = ""
    if spec.draft:
        draft = el(
            "details",
            {"class": "draft", "open": True},
            el("summary", None, text(spec.ui.draft_label)),
            el("pre", None, text(spec.draft)),
        )
    context_panel = ""
    if spec.context:
        context_panel = el(
            "section",
            {"class": "form-context", "aria-labelledby": "form-context-title"},
            el("h2", {"id": "form-context-title"}, text(spec.ui.context_label)),
            el("p", None, text(spec.context)),
        )
    actions = el(
        "div",
        {"class": "actions"},
        el("p", {"class": "form-error", "id": "form-error", "role": "alert"}),
        el("button", {"class": "save", "type": "submit"}, text(spec.ui.save_label)),
    )
    form = el(
        "form",
        {
            "method": "post",
            "action": "",
            "id": "intake-form",
            "novalidate": True,
            "data-validation-message": spec.ui.validation_message,
            "data-saving-label": spec.ui.saving_label,
        },
        *section_cards,
        actions,
    )
    page = PAGE_TEMPLATE.substitute(
        language=html.escape(spec.language, quote=True),
        title=text(spec.title),
        css=CSS,
        progress_label=text(spec.ui.progress_label),
        app_label=text(spec.ui.app_label),
        total_questions=total_questions,
        nav_items="".join(nav_items),
        round_label=text(spec.ui.round_label),
        round_number=spec.round,
        max_rounds=MAX_ROUNDS,
        intro=text(spec.intro),
        context=context_panel,
        draft=draft,
        form=form,
        script=SCRIPT,
    )
    return page.encode("utf-8")


def render_message_page(title: str, message: str, success: bool = False, language: str = "en") -> bytes:
    page = MESSAGE_TEMPLATE.substitute(
        language=html.escape(language, quote=True),
        title=text(title),
        message=text(message),
        css=MESSAGE_CSS,
        status_class="success" if success else "error",
    )
    return page.encode("utf-8")
