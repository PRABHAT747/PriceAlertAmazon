import re

def is_valid_amazon_url(url: str):
    return bool(re.match(r"https://www\.amazon\.in/dp/[A-Z0-9]{10}", url))

def normalize_amazon_url(url: str):
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    if match:
        return f"https://www.amazon.in/dp/{match.group(1)}"
    return url