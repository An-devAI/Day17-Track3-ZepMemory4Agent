# Lab 17 — Submission Notes

## Required analysis

Trong practice set, long-term memory là layer quan trọng nhất vì E02, E03, E08 và E09 đều cần recall facts/preferences qua session, đồng thời E09 kiểm tra user isolation. Context Block của Zep cung cấp managed graph retrieval, relevance và cross-session context; Redis + Qdrant cho nhiều quyền kiểm soát hơn nhưng cần tự xây schema, embedding, ranking, TTL và isolation.

Memory poisoning nên được hạn chế bằng consent trước ingestion, redact PII, namespace theo `user_id`, provenance/source ID, chỉ ghi durable memory từ facts/decisions có bằng chứng, và không cho heartbeat tự cấp quyền hoặc thêm instruction mới. Fact mâu thuẫn cần giữ validity range và ưu tiên fact mới hơn.

Trong benchmark hiện tại, cả bốn layer đều đạt 100% hit rate nên không có layer yếu nhất; short-term đạt E01/E10, long-term đạt E02/E03/E08/E09, episodic đạt E04/E05 và semantic đạt E06/E11. E02 và E03 dùng nhiều token nhất (793 token mỗi case).

E07 là case mixed: long-term phải cung cấp preference Python, còn semantic phải cung cấp rule `Idempotency-Key`; budget manager gộp chúng theo thứ tự short-term → long-term → episodic → semantic. Token reduction không đồng nghĩa retrieval tốt: no-memory có thể trả ít token vì không retrieve gì, nhưng hit rate thấp vì thiếu evidence.

E08 minh họa recency wins: preference TypeScript/NestJS mới phải được ưu tiên hơn preference cũ. E10 minh họa compaction: summary, durable notes và recent turns giữ lại constraint/deadline quan trọng trong khi loại bỏ transcript cũ.

