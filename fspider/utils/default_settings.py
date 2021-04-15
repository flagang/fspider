WORKERS = 10
scheduler_cls = 'fspider.scheduler.PyScheduler'
DOWNLOADER_MIDDLEWARES = {
    'fspider.downloadermiddlewares.down.DefaultDownloaderMiddleware': 999,
}
