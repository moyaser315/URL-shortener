import hashlib
from urllib.parse import urlparse
import re

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


def create_new_url(url: str):
    hashed, length = url_short(url)
    new_url = encode_hash(hashed)
    return new_url


def valid_url(url):
    check_url = urlparse(url)
    return all([check_url.scheme, check_url.netloc])


def parse_user_agent(user_agent):
    os_patterns = {
        "Windows": r"Windows NT [0-9.]+",
        "MacOS": r"Mac OS X [0-9_]+",
        "Android": r"Android [0-9.]+",
        "iOS": r"iPhone OS [0-9_]+|iPad; CPU OS [0-9_]+",
    }
    browser_patterns = {
        "Chrome": r"Chrome/[0-9.]+",
        "Safari": r"Version/[0-9.]+ Safari",
        "Firefox": r"Firefox/[0-9.]+",
    }
    os = next((os for os, pattern in os_patterns.items() if re.search(pattern, user_agent)), "Unknown")
    browser = next((browser for browser, pattern in browser_patterns.items() if re.search(pattern, user_agent)), "Unknown")

    device_type = (
        "Mobile" if "Mobile" in user_agent else "Tablet" if "Tablet" in user_agent else "Desktop"
    )

    return {'os':os, 'browser':browser, 'device':device_type}


if __name__ == '__main__':
    x,y = url_short('https://stackoverflow.com/questions/55858527/how-to-set-the-default-value-of-a-column-in-sqlalchemy-to-the-value-of-a-column')
    _ = encode_hash(x)
    print(x)
    print(decode(_,y))
    _ = valid_url('https://stackoverflow.com/questions/55858527/how-to-set-the-default-value-of-a-column-in-sqlalchemy-to-the-value-of-a-column')
    print(_)
    user_agent_string = "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
    os, browser, device_type = parse_user_agent(user_agent_string)
    print(f"OS: {os}, Browser: {browser}, Device Type: {device_type}")

