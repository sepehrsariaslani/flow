# Flow Persian Phase 1 Design

## Goal

Make Flow usable for Persian-speaking ERP users by improving three things together:

1. Persian query understanding for common ERP intents.
2. Lower-friction autonomous discovery before the agent asks the user follow-up questions.
3. Persian-first copy in the Flow panel and default assistant behavior.

This phase is specifically aimed at requests like `کیک‌های انبارم را بگو` where the current system fails because it searches English DocType names too literally, does not explore enough fallback paths, and asks the user for clarification too early.

## Problem Statement

Current Flow behavior has three coupled weaknesses:

1. Built-in discovery tools are English-centric.
   `find_doctypes()` searches only `DocType.name`, which is not enough for Persian labels, translations, or common business vocabulary.
2. The default `Flow` assistant prompt is English-centric and conservative in the wrong place.
   It tells the model not to guess, but it does not give it a structured exploration path for Persian ERP requests.
3. The UI copy and tool status labels are mostly English.
   Even when the model can answer, the surrounding experience still feels foreign to Persian operators.

The result is an assistant that often stops early and asks vague questions instead of discovering likely matches by itself.

## User Outcomes

After this phase:

- A Persian-speaking user can ask for inventory, items, warehouses, customers, invoices, or similar concepts in Persian.
- Flow will attempt several discovery steps automatically before asking for clarification.
- If no exact result exists, Flow will report what it searched and show the nearest candidates instead of failing vaguely.
- The default assistant responses and primary Flow panel labels will be Persian-first.

## Non-Goals

This phase does not include:

- Hermes-style memory.
- Hermes-style skill runtime or orchestration.
- Major session/kanban/toolset architecture changes.
- Full-desk or full-ERPNext Persian translation work outside Flow.
- Advanced multilingual embeddings or new RAG infrastructure.

## Recommended Approach

Implement a Persian-aware discovery layer inside Flow, then wire the default assistant to use it, then localize the visible Flow panel copy that users see during interaction.

This is preferred over prompt-only changes because prompt-only tuning cannot fix the underlying discovery gap in the built-in tools.

## Alternative Approaches Considered

### 1. Prompt-only tuning

Change only the default assistant instructions so it tries harder before asking questions.

Why not chosen:

- It may reduce some unnecessary questions.
- It does not solve Persian lookup against DocTypes, fields, or records.
- It remains brittle and model-dependent.

### 2. UI-only Persian localization

Translate the panel labels and status copy without changing backend discovery.

Why not chosen:

- It improves appearance but not usefulness.
- Users would still hit the same discovery failures for Persian business requests.

### 3. Full Hermes-style feature port

Try to bring in memory, skill routing, and richer runtime behavior immediately.

Why not chosen:

- Too broad for the current pain point.
- High implementation and integration risk.
- Delays the fix for the actual production problem.

## Architecture

### 1. Persian ERP Resolver

Add a backend resolver responsible for mapping Persian business words to likely ERP structures.

Responsibilities:

- Normalize Persian input.
- Expand common ERP synonyms and aliases.
- Produce likely DocType candidates.
- Produce likely field candidates for record search.
- Produce query hints and fallback search terms.

Examples:

- `انبار` -> `Warehouse`, `Bin`, `Stock Ledger Entry`
- `موجودی` -> `Bin`, `Stock Ledger Entry`, quantity-related fields
- `کالا` / `محصول` -> `Item`
- `کیک` -> search hint for item name/code/barcode/category-style fields

This resolver should be deterministic and lightweight. It should not call the model.

### 2. Persian-aware Discovery Tools

Extend Flow’s existing discovery path instead of inventing a separate agent runtime.

Core changes:

- `find_doctypes()` should support Persian-friendly matching instead of raw English-name substring only.
- Record discovery for ERP-heavy requests should use structured fallback search across likely fields.
- Common ERPNext flows should get explicit fallback paths:
  - inventory lookup
  - item lookup
  - warehouse lookup

For item-like searches, the system should try fields such as:

- `item_name`
- `item_code`
- `barcode`
- translated label-aware or alias-aware matches where available

### 3. Default Assistant Behavior

Update the built-in `Flow` assistant instructions so it behaves more like a proactive operator.

Required behavior:

- Default reply language is Persian unless the user asks otherwise.
- Before asking a clarification question, the assistant must perform multiple discovery attempts.
- If multiple near matches exist, the assistant should present them briefly and ask one precise question.
- If no match exists, the assistant should report what was searched and where.

This should reduce the current “ask too early” behavior while still preserving the “never invent names” rule.

### 4. Flow Panel Persian Copy

Translate Flow panel copy that is directly experienced by users during chat.

Scope includes:

- primary button/status/tool labels in the panel
- tool activity labels
- yes/no style UI words
- key interaction text shown during runs

Scope excludes:

- all Frappe Desk copy
- all ERPNext copy
- broad product-wide translation work outside Flow

## Data and Matching Strategy

### Input Normalization

Normalize:

- Arabic/Persian letter variants
- extra whitespace
- punctuation noise
- half-space edge cases where practical

### Alias Expansion

Maintain a curated alias map for business vocabulary commonly used in this ERP deployment.

Initial categories:

- inventory and warehouse concepts
- products/items
- sales and purchase documents
- customer and supplier concepts

The alias map should be code-based for this phase, not user-configurable yet.

### Discovery Order

For ambiguous Persian requests:

1. resolve likely DocTypes and fields from aliases
2. search likely records using those hints
3. widen search across known ERP fallbacks
4. report nearest results
5. only then ask one precise clarification question if still needed

## Error Handling

When no result is found, the assistant must not stop at “I could not find it.”

It should state:

- which business object it assumed
- which records or fields it searched
- whether it found near matches
- the shortest next clarification question if one is still necessary

When permissions block access, the assistant should say so explicitly in Persian rather than presenting the failure as a search miss.

## Testing Strategy

### Backend

Add tests for:

- Persian normalization
- alias resolution
- Persian-aware DocType candidate lookup
- item/inventory fallback behavior
- “ask later, not earlier” assistant behavior where applicable through deterministic tests

### Integration

Add tests or scripted checks for scenarios like:

- `کیک‌های انبارم را بگو`
- `موجودی اوریو را بگو`
- `انبارها را نشان بده`
- `کالاهای شامل کیک`

The expected result is not always a final business answer; it may be a structured near-match report. The critical requirement is that the system explores first and asks fewer, sharper questions.

### UI

Verify the panel shows Persian translations for the targeted Flow-local copy and that the translated labels do not break layout.

## File/Component Impact

Expected areas of change:

- backend tool/discovery logic
- built-in assistant instructions
- frontend translation/copy helpers and Flow panel components

No architectural rewrite of sessions, memory, or triggers is required for this phase.

## Rollout Strategy

1. Add Persian resolver and discovery support.
2. Update the built-in assistant instructions to use it correctly.
3. Translate Flow panel copy.
4. Validate against the live Persian inventory/product scenarios.

## Risks

### Overfitting to one ERP vocabulary

The alias map may initially reflect this deployment’s wording more than generic ERPNext language.

Mitigation:

- keep aliases grouped and easy to extend
- bias first implementation toward common ERPNext concepts

### False positives in broad record matching

Aggressive contains-search may return noisy results.

Mitigation:

- use ordered fallback fields
- keep result sets bounded
- prefer nearest-candidate reporting over silent guessing

### Prompt drift without deterministic support

If the assistant instructions are improved without enough backend structure, behavior may vary by model.

Mitigation:

- keep key discovery logic in deterministic backend helpers
- use prompt changes to direct sequence, not to replace resolution logic

## Success Criteria

Phase 1 is successful when:

- the default Flow assistant handles common Persian ERP requests substantially better than before
- it performs multi-step discovery before asking the user for clarification
- targeted Flow panel copy is Persian
- the production scenario around Persian inventory/item lookup is materially improved
