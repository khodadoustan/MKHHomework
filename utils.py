import random
import string

import redis


def set_cache(_key, _val, _exp):
    r = redis.Redis(host='cache', port=6379, db=0)
    r.setex(_key, _exp, _val)


def check_key(_key):
    r = redis.Redis(host='cache', port=6379, db=0)
    return bool(r.exists(_key))


def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
