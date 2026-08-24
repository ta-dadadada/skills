# Local Intake Protocol

Read this reference whenever creating, resuming, or serving a local intake.
The Markdown file is both the human-readable working record and the only
persistent machine input. Temporary server tokens and rendered HTML stay in
memory.

## Working document

Create the project-root file with this structure. The marker and field labels
are protocol, while prose below the headings follows the user's language.

```markdown
<!-- LOCAL-INTAKE:STATE:v1 -->
# Local Intake (temporary)

Status: collecting
Round: 0/3

## Working brief

<Current synthesis, with unknowns labelled>

## Decisions

<Recorded user decisions, or omit entries when none exist>

## Blocking open questions

<Questions whose answers can materially change the brief>

## Interview log

<!-- LOCAL-INTAKE:FORM:BEGIN -->
{ ... form JSON ... }
<!-- LOCAL-INTAKE:FORM:END -->
```

Allowed status values are `collecting`, `reviewing`, `agreed`, and
`unresolved`. Set `Round` to the number of submitted forms. A pending form's
`round` must be exactly one greater.

Keep exactly one state marker and at most one pending-form block. The server
replaces the pending block with a rendered interview-log entry after a valid
submission. The agent updates the brief, decisions, open questions, status,
and round count after rereading that entry.

## Form schema

The content between the pending-form markers is one JSON object:

```json
{
  "version": 1,
  "round": 1,
  "mode": "intake",
  "language": "en",
  "title": "Clarify the request",
  "intro": "Answer what you know. Unknown and delegated answers are valid.",
  "context": "The request must remain local and should replace a long clarification chat. No implementation decisions have been agreed yet.",
  "draft": "Optional complete brief shown during review rounds.",
  "ui": {
    "app_label": "Local intake",
    "round_label": "Round",
    "progress_label": "Answered",
    "required_label": "Required",
    "optional_label": "Optional",
    "other_label": "Other",
    "context_label": "Context",
    "draft_label": "Current brief",
    "save_label": "Save answers",
    "saving_label": "Saving...",
    "saved_title": "Answers saved",
    "saved_message": "Return to the conversation.",
    "validation_message": "Complete the highlighted questions."
  },
  "sections": [
    {
      "id": "purpose",
      "title": "Purpose",
      "description": "What should change and why",
      "questions": [
        {
          "id": "desired-outcome",
          "prompt": "What should be different when this is complete?",
          "context": "This answer fixes the intake's goal and determines which later constraints are relevant.",
          "help": "Describe an observable result.",
          "type": "long_text",
          "required": true,
          "placeholder": "The result is..."
        }
      ]
    }
  ]
}
```

`version` is `1`; `round` is `1`, `2`, or `3`; `mode` is `intake` or
`review`; and `language` is a BCP-47-style language tag such as `en` or `ja`.
`draft` is required for review mode. All visible form and success strings,
including the `ui` values, use the user's language. IDs match
`^[A-Za-z][A-Za-z0-9_-]{0,63}$` and question IDs are unique across the form.

`context` is optional at both the form and question levels. Use the
form-level value for shared facts, the current situation, constraints already
known, and the decision background a respondent needs before answering. Use a
question-level value only for facts specific to that question, why the answer
is being requested, or which decision it can change. Do not duplicate the
shared context across questions. Keep `intro` for a short welcome and response
guidance, and keep `help` for answer-format guidance. Context is rendered as
escaped plain text; line breaks are preserved, but HTML and Markdown are not
interpreted.

Question types:

| Type | Additional fields | Recorded answer |
|---|---|---|
| `short_text` | optional `placeholder` | one string |
| `long_text` | optional `placeholder` | one string |
| `single_choice` | non-empty string `options`; optional `allow_other` | one string |
| `multiple_choice` | non-empty string `options`; optional `allow_other` | a list of strings |

Every question has `id`, `prompt`, `type`, and boolean `required`. `context`
and `help` are optional. Option labels are the recorded values. When an
uncertainty choice is relevant, include it explicitly in `options`; the
server does not invent semantic choices.

The UI object is optional as a whole and each missing key falls back to an
English label. Keep action labels literal: the save button describes saving,
and the saved message tells the user what to do next.

## Server command

First inspect any existing path and confirm that it is absent or carries this
protocol's ownership marker. Do not hide an unowned same-name file. After
that check and before creating or updating the working document, run the
bundled entry point from the skill directory to register the path in Git's
local exclude:

```bash
python3 scripts/serve_form.py --document <project-root>/.agent-intake.local.md --prepare
```

Preparation does not require or create the document and is idempotent. Skip it
only when the caller already arranged an equivalent local ignore or the
project is not a Git worktree. This ordering keeps the temporary file out of
`git status` from the moment it is created.

After writing a valid pending form, serve it with:

```bash
python3 scripts/serve_form.py --document <project-root>/.agent-intake.local.md
```

Before serving, the CLI adds the document's repository-relative path to
Git's local `info/exclude` file. This never changes `.gitignore`. When the
caller already manages the temporary path another way, pass
`--no-git-exclude`. The HTTP server itself has no Git side effects.

## Review contract

Round one uses `mode: intake` and covers the known decision surface. Round two
uses `mode: review`, includes the complete draft, and contains an explicit
required single choice for approval or revision. Round three has the same
review contract and exists only after a revision or newly exposed blocker.

The agent may call an intake `agreed` only after an approval response applies
to the complete draft shown in that review form and no blocking open question
remains.
