WORKERS = 10
scheduler_cls = 'fspider.scheduler.PyScheduler'
DOWNLOADER_MIDDLEWARES = {
    # 'fspiderdownloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    # 'fspiderdownloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    # 'fspiderdownloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    # 'fspiderdownloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    # 'fspiderdownloadermiddlewares.useragent.UserAgentMiddleware': 500,
    # 'fspiderdownloadermiddlewares.retry.RetryMiddleware': 550,
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
    #     'fspiderspidermiddlewares.depth.DepthMiddleware': 900,
}
