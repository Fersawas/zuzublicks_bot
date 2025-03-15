import aiohttp
import re
import logging
from lxml import html


async def parse_url(url, xpath):
    url_pattern = r"\d+\.\d+"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                page = await response.text()

                tree = html.fromstring(page)
                elements = tree.xpath(xpath)

                result = []
                for elem in elements:
                    page = elem.text_content() if elem is not None else ""
                    matches = re.findall(url_pattern, page)
                    if matches:
                        result.extend([float(x) for x in matches])
                return result
    except Exception as e:
        logging.error(str(e))
        return []
