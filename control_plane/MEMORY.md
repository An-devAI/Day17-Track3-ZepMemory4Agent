# MEMORY.md

## Durable memory schema

Each durable record should be understandable as:

- scope: user, org, or shared domain
- type: preference, fact, decision, open_loop, episode, semantic_page
- content: the remembered statement
- source: thread/message/document identifier
- timestamp: when the source was observed
- confidence: extraction confidence or review status
- ttl: optional retention period
- validity: current, superseded, or expired

## Recall priority

1. Recent short-term context
2. Long-term user facts/preferences
3. Relevant episodes/reflections
4. Semantic/domain knowledge

## Conflict rule

Use recency plus scope. A project-specific new constraint can override a generic preference for that project without deleting the older preference from unrelated scopes.
