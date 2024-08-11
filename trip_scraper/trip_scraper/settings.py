BOT_NAME = "trip_scraper"

SPIDER_MODULES = ["trip_scraper.spiders"]
NEWSPIDER_MODULE = "trip_scraper.spiders"

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   "trip_scraper.pipelines.HotelscrapPipeline": 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"