from argon2.low_level import hash_secret, Type
# This is AI I couldnt be bothered to figure this out <3
def hash(password: str) -> str:
    password_bytes = password.encode("utf-8")

    result = hash_secret(
        secret=password_bytes,
        salt=password_bytes,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID
    )

    return result.decode("utf-8")