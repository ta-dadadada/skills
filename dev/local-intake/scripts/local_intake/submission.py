"""HTTPフォーム値を検証済み回答へ変換する。"""

from __future__ import annotations

from dataclasses import dataclass

from .spec import FormSpec, Question, RESERVED_OTHER_VALUE


OTHER_VALUE = RESERVED_OTHER_VALUE


class SubmissionError(ValueError):
    """送信内容がフォーム定義に一致していない。"""

    def __init__(self, message: str, question_ids: list[str] | None = None) -> None:
        super().__init__(message)
        self.question_ids = question_ids or []


@dataclass(frozen=True)
class Answers:
    values: dict[str, str | tuple[str, ...]]

    def __getitem__(self, question_id: str) -> str | tuple[str, ...]:
        return self.values[question_id]


def _strict_values(question: Question, payload: dict[str, list[str]]) -> list[str]:
    values = [value.strip() for value in payload.get(question.id, [])]
    if question.type in {"short_text", "long_text", "single_choice"} and len(values) > 1:
        raise SubmissionError("submission repeats a single-value field", [question.id])
    return values


def _choice_value(question: Question, value: str, other_text: str) -> str:
    if value == OTHER_VALUE:
        if not question.allow_other:
            raise SubmissionError("submission uses Other where it is disabled", [question.id])
        if not other_text:
            raise SubmissionError("submission selects Other without text", [question.id])
        return other_text
    if value not in question.options:
        raise SubmissionError("submission contains an unknown choice", [question.id])
    return value


def normalize_submission(spec: FormSpec, payload: dict[str, list[str]]) -> Answers:
    """入力を厳密に検証し、既定値を含まない型付き回答へ変換する。"""

    questions = tuple(spec.questions())
    allowed_fields = {question.id for question in questions}
    allowed_fields.update(f"{question.id}__other_text" for question in questions if question.allow_other)
    unknown_fields = set(payload) - allowed_fields
    if unknown_fields:
        raise SubmissionError(f"submission contains an unknown field: {sorted(unknown_fields)[0]}")

    answers: dict[str, str | tuple[str, ...]] = {}
    missing: list[str] = []
    for question in questions:
        values = _strict_values(question, payload)
        if question.type in {"short_text", "long_text"}:
            value = values[0] if values else ""
            if question.required and not value:
                missing.append(question.id)
            answers[question.id] = value
            continue

        other_text = payload.get(f"{question.id}__other_text", [""])[0].strip()
        if question.type == "single_choice":
            if not values or not values[0]:
                if question.required:
                    missing.append(question.id)
                answers[question.id] = ""
                continue
            answers[question.id] = _choice_value(question, values[0], other_text)
            continue

        selected: list[str] = []
        seen_raw: set[str] = set()
        for raw_value in values:
            if raw_value in seen_raw:
                raise SubmissionError("submission repeats a multiple-choice value", [question.id])
            seen_raw.add(raw_value)
            selected.append(_choice_value(question, raw_value, other_text))
        if question.required and not selected:
            missing.append(question.id)
        answers[question.id] = tuple(selected)

    if missing:
        raise SubmissionError("submission has missing required answers", missing)
    return Answers(answers)
