# L4-005 — Caching

This module introduces Redis caching, cache-aside architecture, and cache invalidation strategies.

---

## Topics Covered

- Redis Fundamentals
- Cache Aside Pattern
- Cache Invalidation

---

## Files

| File | Description |
|------|-------------|
| `l4_005_redis_fundamentals.py` | Connect to Redis and perform SET, GET, MGET, DELETE, TTL, and EXPIRE operations. |
| `l4_005_cache_aside.py` | Implement the Cache-Aside pattern using Redis and PostgreSQL. |
| `l4_005_cache_invalidation.py` | Update PostgreSQL data and invalidate stale Redis cache. |

---

## Install Dependencies

```bash
python3 -m pip install redis
```

---

## Start Redis

```bash
brew services start redis
```

Verify Redis is running:

```bash
redis-cli ping
```

Expected output:

```text
PONG
```

---

## Run Examples

### Redis Fundamentals

```bash
python3 l4_005_redis_fundamentals.py
```

### Cache Aside

```bash
python3 l4_005_cache_aside.py
```

### Cache Invalidation

```bash
python3 l4_005_cache_invalidation.py
```

---

## Cache Flow

### Cache Aside

```text
HTTP Request
      ↓
Check Redis
      ↓
Cache Hit?
  ↓           ↓
Yes          No
 ↓            ↓
Return     PostgreSQL
              ↓
        Store in Redis
              ↓
         Return Response
```

### Cache Invalidation

```text
Update PostgreSQL
        ↓
Delete Redis Cache
        ↓
Next Request
        ↓
Cache Miss
        ↓
Read PostgreSQL
        ↓
Store Fresh Data In Redis
```