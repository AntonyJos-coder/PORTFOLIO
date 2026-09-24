from django.core.cache import cache

HOME_CACHE_KEY = "portfolio_home_v1"


def invalidate_home_cache():
    cache.delete(HOME_CACHE_KEY)
