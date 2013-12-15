import random
import string


def get_random_str():
    return ''.join(random.sample(string.ascii_lowercase,
                   random.randint(10, 15)))
