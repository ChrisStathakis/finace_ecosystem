from django.db import models
from django.shortcuts import reverse
import feedparser
import re
from datetime import datetime
import xml.etree.ElementTree  as ET
import requests
from io import StringIO

from tickers.models import Ticker
from .rss_helper import WordEditor
from .rss_analyzer import RssAnalyzer


RSS_URL = [
    "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    "https://www.ft.com/rss/home/uk",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"
]


ECONOMIST_ENDPOINTS = [
    "https://www.economist.com/the-world-this-week/rss.xml",
    "https://www.economist.com/finance-and-economics/rss.xml",
    "https://www.economist.com/business/rss.xml"

]


def find_words(text: str) -> list:
    words = re.findall(r'\b\w+\b', text)
    return words


class RssFeed(models.Model):
    CHOICES = (
        ("P", "POSITIVE"),
        ("N", "NEGATIVE"),
        ("A", "NEUTRAL")
    )
    title = models.CharField(max_length=255)
    rss_id = models.CharField(max_length=200, unique=True)
    published = models.DateTimeField()
    summary = models.TextField()
    tickers = models.ManyToManyField(Ticker, related_name="rss")
    is_analysed = models.BooleanField(default=False)
    is_positive = models.CharField(choices=CHOICES, default="A")

    def __str__(self):
        return self.title

    def tag_tickers(self):
        return " ".join(ticker.ticker for ticker in self.tickers.all())

    @staticmethod
    def fetch_xml_website():
        endpoint = RSS_URL[0]
        response = requests.get(endpoint)
        response.raise_for_status()

        root = ET.fromstring(response.text)

        for element in root.iter():
            print(element.items)
            print("--------------------------------------")

    @staticmethod
    def fetch_economist_data():
        for endpoint in ECONOMIST_ENDPOINTS:
            d = feedparser.parse(endpoint)
            for feed in d.entries[:10]:
                feed_id = feed.guid.split("content/")[1]
                exists = RssFeed.objects.filter(rss_id=feed_id).exists()
                if not exists:
                    RssFeed.objects.create(
                        title=feed.title,
                        published=datetime.now(),
                        summary=feed.description,
                        rss_id=feed_id
                    )

    @staticmethod
    def create_data():
        # downloads the new rss. It's better for use every day or some hours period
        for endpoint in RSS_URL:
            d = feedparser.parse(endpoint)

            for feed in d.entries:
                exists = RssFeed.objects.filter(rss_id=feed.id).exists()
                if exists:
                    continue
                else:
                    try:
                        RssFeed.objects.create(
                            rss_id=feed.id,
                            title=feed.title,
                            published=datetime.now(),
                            summary=feed.summary
                        )
                    except:
                        continue


    @staticmethod
    def analysis_rss_feed(qs):
        """
            We call all the no analysed rss, after that we initialize the analyzer and
            we check if any ticker is relevant  and if is positive etc
        """

        analyzer = RssAnalyzer()
        for ele in qs:
            print(analyzer.textblob_sentimental_analysis(ele.title))
            print(ele.id, ele.title)
            # is_positive = analyzer.textblob_sentimental_analysis(ele.title)
            ele.is_positive = analyzer.llm_check_if_positive(ele.title)
            entities = analyzer.find_entities(ele.title)
            qs = Ticker.search_entities(entities)
            for ticker in qs:
                ele.tickers.add(ticker)
            ele.save()


    def get_absolute_url(self):
        return reverse('rss:detail_view', kwargs={'pk': self.id})
