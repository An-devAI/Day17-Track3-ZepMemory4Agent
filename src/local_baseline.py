from __future__ import annotations

import json
import uuid

import redis
from qdrant_client import QdrantClient, models
from sklearn.feature_extraction.text import HashingVectorizer

from .config import settings
from .utils import load_knowledge

COLLECTION = "lab17_local_semantic"
VECTOR_SIZE = 256


def demo_redis() -> None:
    client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    client.ping()

    profile_key = "lab17:user:minh-lab17:profile"
    facts_key = "lab17:user:minh-lab17:facts"
    sessions_key = "lab17:user:minh-lab17:recent_sessions"

    client.hset(
        profile_key,
        mapping={
            "preferred_language": "Python",
            "avoid_language": "Java",
            "style": "short examples",
        },
    )
    client.expire(profile_key, 90 * 24 * 3600)
    client.sadd(facts_key, "project=ORCHID-27", "learning=async-await")
    client.expire(facts_key, 30 * 24 * 3600)
    client.delete(sessions_key)
    client.rpush(sessions_key, "minh-s1", "minh-s2")
    client.expire(sessions_key, 7 * 24 * 3600)

    print("[Redis baseline]")
    print("profile:", client.hgetall(profile_key))
    print("facts:", sorted(client.smembers(facts_key)))
    print("recent sessions:", client.lrange(sessions_key, 0, -1))
    print("ttl(profile):", client.ttl(profile_key), "seconds")


def vectorizer() -> HashingVectorizer:
    return HashingVectorizer(
        n_features=VECTOR_SIZE,
        alternate_sign=False,
        norm="l2",
        lowercase=True,
    )


def demo_qdrant() -> None:
    client = QdrantClient(url=settings.qdrant_url)
    if client.collection_exists(COLLECTION):
        client.delete_collection(COLLECTION)
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
    )

    docs = load_knowledge()
    texts = [json.dumps(doc, ensure_ascii=False) for doc in docs]
    vecs = vectorizer().transform(texts).toarray()
    points = []
    for doc, vec in zip(docs, vecs, strict=True):
        points.append(
            models.PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_URL, doc["id"])),
                vector=vec.tolist(),
                payload=doc,
            )
        )
    client.upsert(collection_name=COLLECTION, points=points, wait=True)

    query = "payment POST retry idempotency exponential backoff"
    query_vec = vectorizer().transform([query]).toarray()[0].tolist()
    hits = client.query_points(
        collection_name=COLLECTION,
        query=query_vec,
        limit=3,
        with_payload=True,
    ).points

    print("\n[Qdrant local semantic baseline]")
    print("query:", query)
    for hit in hits:
        print(f"score={hit.score:.3f} payload={hit.payload}")


def main() -> None:
    demo_redis()
    demo_qdrant()
    print("\nThis baseline is intentionally simple: students use Zep for the main lab.")


if __name__ == "__main__":
    main()
