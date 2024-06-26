from django.db import models
from django.shortcuts import reverse
import feedparser
import re
from datetime import datetime

from tickers.models import Ticker
from .rss_helper import WordEditor
from .rss_analyzer import RssAnalyzer

RSS_URL = ["https://feeds.content.dowjones.io/public/rss/mw_topstories",
            "https://www.ft.com/rss/home/uk",
            "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"
            ]



def find_words(text: str) -> list:
    words = re.findall(r'\b\w+\b', text)
    return words


class RssFeed(models.Model):
    title = models.CharField(max_length=255)
    rss_id = models.CharField(max_length=200, unique=True)
    published = models.DateTimeField()
    summary = models.TextField()
    tickers = models.ManyToManyField(Ticker)
    is_analysed = models.BooleanField(default=False)
    is_positive = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def tag_tickers(self):
        return " ".join(ticker.ticker for ticker in self.tickers.all())

    @staticmethod
    def create_data():
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

    def rss_find_ticker(self):
        analyzer = RssAnalyzer()
        tickers_str = analyzer.find_tickers(title=self.title)
        qs = Ticker.objects.filter(title__in=tickers_str)
        print(qs)
        print(tickers_str, qs)
        for ticker in qs:
            self.tickers.add(ticker)
        self.save()
        print("Find Ticker is done")

        
    @staticmethod
    def analysis_rss_feed():
        qs = RssFeed.objects.filter(is_analysed=False)
        analyzer = RssAnalyzer()
        analyzer.load_dataset()
        analyzer.train_dataset()
        for ele in qs:
            result = analyzer.predict_rss(ele)
            print(f'{ele.title} -----  Predict{result}')
            ele.rss_find_ticker()
        



    def get_absolute_url(self):
        return reverse('rss:detail_view', kwargs={'pk': self.id})
