from urllib.parse import quote


def encoded_url(url):
    """
    对url进行编码
    Args:
        url:

    Returns:

    """
    return quote(url, safe=':/?=&')
