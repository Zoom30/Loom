import hashlib

SHARDS = 1


def shard_for(exec_id: str) -> str:
    digest = hashlib.sha1(exec_id.encode()).hexdigest()
    n = int(digest, 16)
    bucket = n % SHARDS
    return f"DUE#{bucket}"
