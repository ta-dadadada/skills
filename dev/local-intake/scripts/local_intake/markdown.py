"""検証済み回答をMarkdownログへ変換する。"""

from __future__ import annotations

import datetime as dt

from .spec import FormSpec
from .submission import Answers


def quote_markdown(value: str, first_prefix: str = "> ", continuation_prefix: str = "> ") -> list[str]:
    lines = value.splitlines() or [""]
    return [f"{first_prefix}{lines[0]}", *[f"{continuation_prefix}{line}" for line in lines[1:]]]


def render_log_entry(spec: FormSpec, answers: Answers) -> str:
    """回答を構造を壊さないMarkdownログへ変換する。"""

    timestamp = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    lines = [
        f"### Round {spec.round}: {spec.title}",
        "",
        f"_Answered: {timestamp} | mode: `{spec.mode}`_",
        "",
    ]
    for section in spec.sections:
        lines.extend([f"#### {section.title}", ""])
        for question in section.questions:
            prompt = " ".join(question.prompt.splitlines())
            lines.extend([f"- **{prompt}** (`{question.id}`)", ""])
            answer = answers[question.id]
            if isinstance(answer, tuple):
                if answer:
                    for item in answer:
                        lines.extend(quote_markdown(item, "> - ", ">   "))
                else:
                    lines.append("> _(No answer)_")
            elif answer:
                lines.extend(quote_markdown(answer))
            else:
                lines.append("> _(No answer)_")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
