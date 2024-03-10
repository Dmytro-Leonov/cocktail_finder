import bcrypt


def check_password(*, plain_password: str, hashed_password: str) -> bool:
    plain_password_bytes = plain_password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


def hash_password(*, password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")
