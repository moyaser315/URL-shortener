import hashlib

base62_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def url_short(orig: str) -> tuple:
    url_hash = hashlib.md5()
    orig = orig.encode(encoding="UTF-8")
    url_hash.update(orig)
    url_hash = url_hash.digest()
    byte_len = len(url_hash)
    return url_hash, byte_len


def encode_hash(hashed_val: str) -> str:

    hashed_val = int.from_bytes(hashed_val, byteorder="big")
    # print(hashed_val)
    ans = ""

    if hashed_val == 0:
        return base62_char[0]
    while hashed_val > 0:
        rem = hashed_val % 62
        ans += base62_char[rem]
        hashed_val //= 62
    # print(ans)
    ans = ans[::-1]
    return ans


def decode(encoded_url: str, byte_len: int) -> str:
    ans = 0

    for i in encoded_url:
        ans = ans * 62 + base62_char.index(i)
    return ans.to_bytes(length=byte_len, byteorder="big")


# TODO: the unhashing for retriving
def create_new_url(url: str):
    hashed, length = url_short(url)
    new_url = encode_hash(hashed)
    return new_url


# x,y = url_short('https://stackoverflow.com/questions/55858527/how-to-set-the-default-value-of-a-column-in-sqlalchemy-to-the-value-of-a-column')
# _ = encode_hash(x)
# print(x)
# print(decode(_,y))
