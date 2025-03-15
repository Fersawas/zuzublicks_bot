import re
import logging

import pandas as pd

from lxml import etree

from constants import ERRORS
from custom_exceptions import (
    ColumnsDoNotMatch,
    InvalidUrlFormat,
    InvalidXPathFormat,
    EmptyData,
)


URL_PATTERN = re.compile(
    r"^(https?://)?" r"([\da-z\.-]+)\.([a-z\.]{2,6})" r"([/\w \.-]*)*" r"/?$"
)


def validate_xpath(xpath):
    try:
        etree.XPath(xpath)
        return 0
    except etree.XPathSyntaxError:
        return 1


def validate_data(file, COLUMNS):
    df = pd.read_excel(file)
    print(df.columns)
    if df.shape[0] == 0:
        logging.warn(ERRORS["empty"])
        raise EmptyData(ERRORS["empty"])

    if len(df.columns) != len(COLUMNS):
        print(len(df.columns) != len(COLUMNS))
        print("YEP")
        logging.warn(ERRORS["columns_len"])
        raise ColumnsDoNotMatch(ERRORS["columns_len"])

    if df.columns.tolist() != COLUMNS:
        print("NOP")
        logging.warn(ERRORS["columns"])
        raise ColumnsDoNotMatch(ERRORS["columns"])

    if df.url.apply(lambda x: 0 if URL_PATTERN.match(x) else 1).sum() > 0:
        logging.warn(ERRORS["url"])
        raise InvalidUrlFormat(ERRORS["url"])

    if df.xpath.apply(validate_xpath).sum() > 0:
        logging.warn(ERRORS["xpath"])
        raise InvalidXPathFormat(ERRORS["xpath"])
    else:
        return df
