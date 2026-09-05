# Page and interaction patterns

Defaults below are conditional recommendations. Explicit product requirements,
task evidence, accessibility, and established system behavior decide exceptions.

## Page archetypes

| Dominant job | Starting structure | Decision boundary |
|---|---|---|
| Find and operate on records | Collection: toolbar, filters, table/list | Use comparison needs to choose representation |
| Inspect many records in sequence | Persistent collection + detail | Preserve selection, filters, and scroll during inspection |
| Work deeply on one record | Record header, properties, content/activity | Give independent work a navigable destination |
| Move work through stages | Queue or board | Choose board when stage and movement matter; table when attributes matter |
| Monitor and decide from aggregates | Dashboard with trends and drill-down | Every metric serves a decision and links to supporting records |
| Review or approve | Object + supporting context + decision actions | Keep evidence and decision consequences visible together |

Choose the entry page from the primary job. Monitoring earns a dashboard;
processing pending work earns a queue. Combine archetypes only when the scenario
requires their simultaneous context.
General configuration, creation, and search structure belongs to the companion
skill; supply business-specific fields and search scope as inputs.

## Action locality

| Affected scope | Placement |
|---|---|
| Collection: create, import/export, search, filter, display | Collection header or toolbar |
| One record | Row or record header/menu |
| One attribute | Field or cell |
| Selected records | Selection toolbar with count and scope |
| Whole application | Application navigation/header |

The companion `frontend-ui-design` skill chooses the interaction surface and
handles responsive/focus behavior. Supply it the required collection context
and the consequence and reversibility of each operation.
