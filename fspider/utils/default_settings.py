WORKERS = 10
scheduler_cls = 'fspider.scheduler.PyScheduler'
DOWNLOADER_MIDDLEWARES = {
    'fspider.downloadermiddlewares.down.DefaultDownloaderMiddleware': 999,
}
SPIDER_MIDDLEWARES = {
    'fspider.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'fspider.spidermiddlewares.depth.DepthMiddleware': 900,
    # 'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    #     'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    #     'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
    #     'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    #     'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
}
