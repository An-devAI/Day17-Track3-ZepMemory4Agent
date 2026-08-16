# MEMORY_SCHEMA.md

Use the schema in MEMORY.md as the contract between extraction, storage, retrieval and deletion.

Recommended fields for custom/local backends:

```json
{
  "scope": "user:minh-lab17",
  "type": "preference",
  "content": "Prefer Python for personal ORCHID-27 demos",
  "source": "thread:minh-s1",
  "timestamp": "2026-08-01T09:00:00Z",
  "confidence": 1.0,
  "ttl_seconds": 7776000,
  "validity": "current"
}
```
