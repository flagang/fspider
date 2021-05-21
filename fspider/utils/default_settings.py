from importlib import import_module

WORKERS = 10
scheduler_cls = 'fspider.scheduler.PyScheduler'
DOWNLOADER_MIDDLEWARES = {
    'fspider.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    # 'fspiderdownloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'fspider.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'fspider.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'fspider.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'fspider.downloadermiddlewares.retry.RetryMiddleware': 550,
    # 'fspiderdownloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    # 'fspiderdownloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    # 'fspiderdownloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    # 'fspiderdownloadermiddlewares.redirect.RedirectMiddleware': 600,
    'fspider.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    # 'fspiderdownloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    # 'fspiderdownloadermiddlewares.stats.DownloaderStats': 850,
    # 'fspiderdownloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
    'fspider.downloadermiddlewares.down.DefaultDownloaderMiddleware': 999,

}
SPIDER_MIDDLEWARES = {
    'fspider.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'fspider.spidermiddlewares.referer.RefererMiddleware': 700,
    'fspider.spidermiddlewares.depth.DepthMiddleware': 900,
    # 'fspiderspidermiddlewares.httperror.HttpErrorMiddleware': 50,
    #     'fspiderspidermiddlewares.offsite.OffsiteMiddleware': 500,
    #     'fspiderspidermiddlewares.urllength.UrlLengthMiddleware': 800,
}
USER_AGENT = f'Fspider/{import_module("fspider").__version__}'

ROBOTSTXT_OBEY = True

RETRY_ENABLED = True
RETRY_TIMES = 2
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
RETRY_PRIORITY_ADJUST = -1
