import random
import string

from .models import URLMap


MAX_ATTEMPTS = 10
DEFAULT_LENGTH = 6

def get_unique_short_id(length: int = None) -> str:
    """
    Генерирует уникальный короткий идентификатор.

    Если length не указана, выбирается случайная длина от 4 до 10 символов.
    """
    chars = string.ascii_letters + string.digits
    
    if length is None:
        length = DEFAULT_LENGTH
    
    for _ in range(MAX_ATTEMPTS):
        short_id = ''.join(random.choice(chars) for _ in range(length))
    
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id

    return get_unique_short_id(length + 1)
