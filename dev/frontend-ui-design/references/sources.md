# Research provenance

Extracted from two user-supplied Japanese productivity-UI research handoffs
(received 2026-09-05). This package generalizes their interaction, input, state,
accessibility requirements, and design review beyond business applications.
Concrete semantics, ARIA, event/focus code, and runtime verification now belong
to `frontend-ui-implementation`; this package defines their expected outcomes.
Record comparison, saved views, and business page archetypes belong to the
separate `business-ui-design` skill.

The reading trail includes Primer's [layout](https://primer.style/product/getting-started/foundations/layout/),
[navigation](https://primer.style/product/ui-patterns/navigation/),
[dialogs](https://primer.style/product/components/dialog/guidelines/),
[action menus](https://primer.style/product/components/action-menu/guidelines/),
[forms](https://primer.style/product/ui-patterns/forms/), and
[empty states](https://primer.style/product/ui-patterns/empty-states/), and
[table accessibility](https://primer.style/product/components/data-table/accessibility/), plus NN/g's
[usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
and [accelerators](https://www.nngroup.com/articles/ui-accelerators/).

These links preserve the handoffs' sources; current page contents were not
independently audited for this package. The workflow and generalization are
synthesis, not verbatim vendor requirements or an accessibility standard.
Consult current primary documentation for exact component APIs and compliance
claims. The product's design system supplies concrete visual values.
