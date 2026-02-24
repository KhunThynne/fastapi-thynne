import secrets
import string


def generate_product_key() -> str:
    chars = string.ascii_uppercase + string.digits
    segments = []
    for _ in range(6):
        segments.append("".join(secrets.choice(chars) for _ in range(4)))
    inner_parts = "-".join(segments)
    suffix = "".join(secrets.choice(chars) for _ in range(3))
    final_key = f"HP-{inner_parts}-{suffix}"
    return final_key
