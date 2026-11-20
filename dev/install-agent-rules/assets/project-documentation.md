# Project Documentation

Write for the reader's next action or decision. Start an installation guide with the shortest working path and a way to recognize success. In a design note, lead with the decision and the constraint that explains it.

Give each fact a clear home. Follow the project's existing conventions. A README can explain what the project does and show a first successful use. A specification can define a supported contract. A contributor guide can explain how to change and verify it. Add a separate document when it serves a distinct reader or maintenance need.

Link to the authoritative source where a reader needs more detail. For a CLI, a README example can show a useful invocation and point to the command's help for the full option list. Repeat a prerequisite or consequence at the point of action when overlooking it would cause a mistake. Keep repeated details small enough to maintain together.

When behaviour changes, trace what a reader would do differently. Update the source that defines the affected fact and the examples or instructions that rely on it. Preserve decision records as history and mark superseded decisions where readers would otherwise mistake them for current guidance.

Check changed commands from the documented working directory, with the stated prerequisites. Verify link destinations and distinguish placeholders from values a reader can use as written. If an example cannot be exercised, identify the unverified part when reporting the change.
