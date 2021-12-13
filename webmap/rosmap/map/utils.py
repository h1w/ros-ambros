from random import choice
from string import ascii_letters, digits

AVAIABLE_CHARS = ascii_letters + digits

def create_random_code(chars=AVAIABLE_CHARS):
    return "".join(
        [choice(chars) for _ in range(8)]
    )

def randomize_slug(slug):
    random_code = create_random_code()
    
    return slug + '-' + random_code
