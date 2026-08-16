# AGENTS.md

## Work rules

- Route every query before retrieval.
- Keep short-term memory thread-scoped.
- Keep long-term facts, preferences and open loops user-scoped unless an org scope is explicit.
- Add semantic/domain knowledge only to the shared standalone graph.
- Do not dump a full transcript into a new thread.
- Durable writes must preserve source, timestamp, confidence and scope when available.
- If current information conflicts with an older fact, prefer the more recent scoped fact and keep provenance.
- Never let a heartbeat/background pass grant itself new permissions.
