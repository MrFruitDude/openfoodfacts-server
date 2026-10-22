import unittest
from datetime import date

from scrapy.http import HtmlResponse

from non_eu_spider import NonEuSpider
from packager_codes import document_info_diff


class NonEuSpiderTest(unittest.TestCase):
    def test_parse_document_without_network(self):
        response = HtmlResponse(
            url="https://example.test/list",
            body=b'<ul class="country-list"><li>'
            b'<a class="country-name">Canada</a><h3>Meat</h3>'
            b'<ul><li><a href="/sample.pdf">Sample'
            b'<span>(22/10/2026)</span></a></li></ul></li></ul>',
            encoding="utf-8",
        )

        items = list(NonEuSpider().parse(response))

        self.assertEqual(len(items), 1)
        item = dict(items[0])
        self.assertEqual(item["country_name"], "Canada")
        self.assertEqual(item["section"], "Meat")
        self.assertEqual(item["title"], "Sample")
        self.assertEqual(item["publication_date"], date(2026, 10, 22))
        self.assertEqual(item["url"], "https://example.test/sample.pdf")
        self.assertEqual(document_info_diff([item], [])["new"], [item])


if __name__ == "__main__":
    unittest.main()
