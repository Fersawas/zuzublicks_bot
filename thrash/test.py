import pandas as pd
import re
from lxml import etree

url = "https://www.ozon.ru/category/noutbuki-15692/"
XPath = '//*[@id="contentScrollPaginator"]/div[1]/div/div/div/div[1]/div[1]/div[1]/div/span[1]'

xpath = '//*[@id="default"]/div/div/div/div/section/div[2]/ol/li[1]/article/div[2]/p[1]'
url = "https://books.toscrape.com/"

df = pd.DataFrame(
    {
        "title": [
            "a",
            "b",
        ],  # "c", "d"],
        "url": [
            "https://books.toscrape.com/",
            "https://books.toscrape.com/",
        ],  # "c", "d"],
        "xpath": [
            '//*[@id="default"]/div/div/div/div/section/div[2]/ol/li[1]/article/div[2]/p[1]',
            '//*[@id="default"]/div/div/div/div/section/div[2]/ol/li[1]/article/div[2]/p[1]',
            # "//div[@id='content'",
            # "//div[@id='content'",
        ],
    }
)

empty = pd.DataFrame({"title": [], "url": [], "xpath": []})
wr_cols = pd.DataFrame({"tittle": ["a"], "urrl": ["b"], "xpathh": ["c"]})
full_empty = pd.DataFrame()


def validate_xpath(xpath):
    try:
        etree.XPath(xpath)
        return 0
    except etree.XPathSyntaxError:
        return 1


URL_PATTERN = re.compile(
    r"^(https?://)?" r"([\da-z\.-]+)\.([a-z\.]{2,6})" r"([/\w \.-]*)*" r"/?$"
)

print(df.url.apply(lambda x: 0 if URL_PATTERN.match(x) else 1).sum())
print(df.xpath.apply(validate_xpath).sum())
df.to_excel("test.xlsx", index=False)
empty.to_excel("empty.xlsx", index=False)
full_empty.to_excel("full_empty.xlsx", index=False)
wr_cols.to_excel("wr_cols.xlsx", index=False)
print(empty.shape[0])

"""
git remote add amvera https://git.amvera.ru/bebabobins/zuzublickbot
git push amvera master
git push

"""
