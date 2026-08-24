"""JSON境界で検証済みフォーム型へ変換する。"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from typing import Iterator


MAX_ROUNDS = 3
MAX_QUESTIONS = 100
QUESTION_TYPES = {"short_text", "long_text", "single_choice", "multiple_choice"}
CHOICE_TYPES = {"single_choice", "multiple_choice"}
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")
LANGUAGE_RE = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")
RESERVED_OTHER_VALUE = "__local_intake_other__"


class ProtocolError(ValueError):
    """作業文書またはフォーム定義が契約に違反している。"""


def _mapping(raw: object, context: str) -> dict:
    if not isinstance(raw, dict):
        raise ProtocolError(f"{context} must be an object")
    return raw


def _required_string(raw: dict, key: str, context: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ProtocolError(f"{context}.{key} must be a non-empty string")
    return value


def _optional_string(raw: dict, key: str, context: str) -> str:
    value = raw.get(key, "")
    if not isinstance(value, str):
        raise ProtocolError(f"{context}.{key} must be a string")
    return value


@dataclass(frozen=True)
class UIStrings:
    app_label: str = "Local intake"
    round_label: str = "Round"
    progress_label: str = "Answered"
    required_label: str = "Required"
    optional_label: str = "Optional"
    other_label: str = "Other"
    context_label: str = "Context"
    draft_label: str = "Current brief"
    save_label: str = "Save answers"
    saving_label: str = "Saving..."
    saved_title: str = "Answers saved"
    saved_message: str = "Return to the conversation."
    validation_message: str = "Complete the highlighted questions."

    @classmethod
    def parse(cls, raw: object, context: str = "form.ui") -> "UIStrings":
        if raw is None:
            return cls()
        mapping = _mapping(raw, context)
        defaults = cls()
        names = {field.name for field in fields(cls)}
        unknown = set(mapping) - names
        if unknown:
            raise ProtocolError(f"{context} contains unknown key: {sorted(unknown)[0]}")
        values = {}
        for name in names:
            value = mapping.get(name, getattr(defaults, name))
            if not isinstance(value, str) or not value.strip():
                raise ProtocolError(f"{context}.{name} must be a non-empty string")
            values[name] = value
        return cls(**values)


@dataclass(frozen=True)
class Question:
    id: str
    prompt: str
    type: str
    required: bool
    context: str = ""
    help: str = ""
    placeholder: str = ""
    options: tuple[str, ...] = ()
    allow_other: bool = False

    @classmethod
    def parse(cls, raw: object, context: str) -> "Question":
        mapping = _mapping(raw, context)
        question_id = _required_string(mapping, "id", context)
        if not ID_RE.fullmatch(question_id):
            raise ProtocolError(f"{context}.id has an invalid format")
        prompt = _required_string(mapping, "prompt", context)
        question_type = mapping.get("type")
        if question_type not in QUESTION_TYPES:
            raise ProtocolError(f"{context}.type is unsupported")
        required = mapping.get("required")
        if type(required) is not bool:
            raise ProtocolError(f"{context}.required must be a boolean")
        allow_other = mapping.get("allow_other", False)
        if type(allow_other) is not bool:
            raise ProtocolError(f"{context}.allow_other must be a boolean")

        raw_options = mapping.get("options")
        options: tuple[str, ...] = ()
        if question_type in CHOICE_TYPES:
            if not isinstance(raw_options, list) or not raw_options:
                raise ProtocolError(f"{context}.options must be a non-empty array")
            if any(not isinstance(option, str) or not option.strip() for option in raw_options):
                raise ProtocolError(f"{context}.options must contain non-empty strings")
            options = tuple(raw_options)
            if len(set(options)) != len(options):
                raise ProtocolError(f"{context}.options must be unique")
            if RESERVED_OTHER_VALUE in options:
                raise ProtocolError(f"{context}.options contains a reserved value")
        elif raw_options is not None:
            raise ProtocolError(f"{context}.options is only valid for choice questions")
        if allow_other and question_type not in CHOICE_TYPES:
            raise ProtocolError(f"{context}.allow_other is only valid for choice questions")

        return cls(
            id=question_id,
            prompt=prompt,
            type=question_type,
            required=required,
            context=_optional_string(mapping, "context", context),
            help=_optional_string(mapping, "help", context),
            placeholder=_optional_string(mapping, "placeholder", context),
            options=options,
            allow_other=allow_other,
        )


@dataclass(frozen=True)
class Section:
    id: str
    title: str
    description: str
    questions: tuple[Question, ...]

    @classmethod
    def parse(cls, raw: object, context: str, question_limit: int = MAX_QUESTIONS) -> "Section":
        mapping = _mapping(raw, context)
        section_id = _required_string(mapping, "id", context)
        if not ID_RE.fullmatch(section_id):
            raise ProtocolError(f"{context}.id has an invalid format")
        raw_questions = mapping.get("questions")
        if not isinstance(raw_questions, list) or not raw_questions:
            raise ProtocolError(f"{context}.questions must be a non-empty array")
        questions: list[Question] = []
        for index, question in enumerate(raw_questions):
            if len(questions) >= question_limit:
                raise ProtocolError(f"form may contain at most {MAX_QUESTIONS} questions")
            questions.append(Question.parse(question, f"{context}.questions[{index}]"))
        return cls(
            id=section_id,
            title=_required_string(mapping, "title", context),
            description=_optional_string(mapping, "description", context),
            questions=tuple(questions),
        )


@dataclass(frozen=True)
class FormSpec:
    version: int
    round: int
    mode: str
    language: str
    title: str
    intro: str
    context: str
    draft: str
    ui: UIStrings
    sections: tuple[Section, ...]

    @classmethod
    def parse(cls, raw: object, context: str = "form") -> "FormSpec":
        mapping = _mapping(raw, context)
        version = mapping.get("version")
        if type(version) is not int or version != 1:
            raise ProtocolError(f"{context}.version must be 1")
        round_number = mapping.get("round")
        if type(round_number) is not int or round_number not in range(1, MAX_ROUNDS + 1):
            raise ProtocolError(f"{context}.round must be between 1 and {MAX_ROUNDS}")
        mode = mapping.get("mode")
        if mode not in {"intake", "review"}:
            raise ProtocolError(f"{context}.mode must be intake or review")
        language = mapping.get("language", "en")
        if not isinstance(language, str) or not LANGUAGE_RE.fullmatch(language):
            raise ProtocolError(f"{context}.language must be a BCP-47-style language tag")
        draft = _optional_string(mapping, "draft", context)
        if mode == "review" and not draft.strip():
            raise ProtocolError(f"{context}.draft is required for review mode")

        raw_sections = mapping.get("sections")
        if not isinstance(raw_sections, list) or not raw_sections:
            raise ProtocolError(f"{context}.sections must be a non-empty array")
        sections: list[Section] = []
        question_count = 0
        for index, raw_section in enumerate(raw_sections):
            section = Section.parse(
                raw_section,
                f"{context}.sections[{index}]",
                question_limit=MAX_QUESTIONS - question_count,
            )
            question_count += len(section.questions)
            if question_count > MAX_QUESTIONS:
                raise ProtocolError(f"{context} may contain at most {MAX_QUESTIONS} questions")
            sections.append(section)

        section_ids = [section.id for section in sections]
        if len(set(section_ids)) != len(section_ids):
            duplicate = next(value for value in section_ids if section_ids.count(value) > 1)
            raise ProtocolError(f"duplicate section id: {duplicate}")
        question_ids = [question.id for section in sections for question in section.questions]
        if len(set(question_ids)) != len(question_ids):
            duplicate = next(value for value in question_ids if question_ids.count(value) > 1)
            raise ProtocolError(f"duplicate question id: {duplicate}")

        return cls(
            version=version,
            round=round_number,
            mode=mode,
            language=language,
            title=_required_string(mapping, "title", context),
            intro=_required_string(mapping, "intro", context),
            context=_optional_string(mapping, "context", context),
            draft=draft,
            ui=UIStrings.parse(mapping.get("ui")),
            sections=tuple(sections),
        )

    def questions(self) -> Iterator[Question]:
        for section in self.sections:
            yield from section.questions
