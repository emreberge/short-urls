import string
ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits + '-_'
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)

def num_encode(n):
    s = []
    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        if n == 0: break
    return ''.join(reversed(s)).rjust(6,ALPHABET[0])

def num_decode(s):
    n = 0
    for c in s:
        if c not in ALPHABET:
            raise ValueError('Char not in ALPHABET')
        n = n * BASE + ALPHABET_REVERSE[c]
    return n
