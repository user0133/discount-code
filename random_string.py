import random
import string

def randStr(chars = string.ascii_uppercase + string.digits, n=10):
    return ''.join(random.choice(chars) for value in range(n))


def create_random_coupon():
    return randStr()
