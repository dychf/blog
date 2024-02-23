from urllib.parse import quote


def encoded_url(url):
    """
    对url进行编码
    """
    return quote(url, safe=':/?=&')


url = 'https://quickchart.io/chart?c={"type": "line", "data": {"labels": ["a", "B", "C"], "datasets": [{"label": "Example", "data": [5, 10, 15]}]}}'



res=encoded_url(url)
print(res)