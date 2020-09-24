from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor

SETTINGS = get_project_settings()


class Runner:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl(self):
        yield self.runner.crawl('pzszerm')
        reactor.stop()

    def run(self):
        self.crawl()
        reactor.run()

runner = Runner()
runner.run()
