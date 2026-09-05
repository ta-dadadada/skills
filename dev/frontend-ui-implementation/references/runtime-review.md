# Runtime review

Run the UI using repository-approved tools. For each applicable check, record
**pass / defect / unverified**, the actual observation and environment, and any
correction. Mark inapplicable checks with a reason. A small fix can inherit
unchanged contracts and focus on affected paths; explicitly account for the
minimum checks below rather than silently claiming full coverage. A partial
path is evidence only for the steps exercised; completion remains unverified
until the scenario reaches its intended outcome through that input method.

| Minimum check | Runtime evidence |
|---|---|
| Primary pointer path | Reach the intended outcome through the standard GUI and actual controls |
| Primary keyboard path | Complete the scenario and recovery with real key input, without pointer assistance |
| Narrow viewport | Record dimensions and exercise the task through the specified layout transition |
| 200% zoom | Set actual browser zoom to 200%, record how it was set/confirmed, and check the task and focus visibility |
| Loading and empty | Exercise pending, empty, and relevant no-match states with honest next steps |
| Relevant error | Trigger a failed load/validation/access case as applicable and exercise recovery |
| Mutation failure | When writes exist, trigger failure, check draft/context retention, and retry or correct |
| Focus | Observe order, visible indicator, transient containment/return, and focus after errors/remounts |
| Names, roles, and states | Inspect the running accessibility tree/computed properties and changes during interaction |
| Repository checks | Run applicable tests, lint, and typecheck; distinguish failures from unavailable commands |
| Domain acceptance | Exercise supplied scope, comparison, navigation, and data-truthfulness cases |

Zoom changes the browser's layout viewport. A narrow viewport, device scale
factor, pinch zoom, or CSS zoom alone is not proof of browser zoom testing.
If automation cannot set/confirm it, record 200% zoom as unverified and name the
pending manual check. For two-dimensional data, check intentional scrolling and
preserved comparison instead of requiring every column to fit.

Use realistic long content. Identify mocks and injected failures as fixtures,
not evidence of real backend integration. Check visible contrast/targets against
the supplied requirements with appropriate measurements when in scope.

Screenshots support visual findings; real key events and active-focus observations
support keyboard claims. Attribute/DOM inspection is static evidence; inspecting
a runtime accessibility tree supports names/roles/state claims in that environment.
Neither demonstrates screen-reader announcements. Exercise assistive technology
when available; otherwise label its behavior **unverified**. Automated accessibility
checks cover only their tested rules, not blanket accessibility compliance.

Fix observed defects and recheck affected cases. In the delivery report distinguish
passed runtime cases, static-only observations, unverified cases, and known defects.
Unavailable runtime tools leave runtime checks unverified; they do not turn code
review into an accessibility verification result.
