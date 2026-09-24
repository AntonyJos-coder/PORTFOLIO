from django.db.models.signals import post_delete, post_save

from .models import Education, Experience, Profile, Project, Skill
from .page_cache import invalidate_home_cache

_WATCHED = (Profile, Education, Skill, Experience, Project)


def _bust_home_cache(sender, **kwargs):
    invalidate_home_cache()


def connect_cache_signals():
    for model in _WATCHED:
        post_save.connect(
            _bust_home_cache,
            sender=model,
            dispatch_uid=f"portfolio_home_save_{model.__name__}",
        )
        post_delete.connect(
            _bust_home_cache,
            sender=model,
            dispatch_uid=f"portfolio_home_delete_{model.__name__}",
        )
