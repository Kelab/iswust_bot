import random
import string


def random_string(
    length: int = 16, chars: str = string.ascii_letters + string.digits
) -> str:
    return "".join(random.choices(chars, k=length))
