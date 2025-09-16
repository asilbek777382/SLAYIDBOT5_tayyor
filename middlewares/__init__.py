from .throttling import SimpleThrottlingMiddleware

def setup_middlewares(dp):
    dp.message.middleware(SimpleThrottlingMiddleware(rate_limit=1.5))
