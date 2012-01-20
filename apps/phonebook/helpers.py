import hashlib
import re
import urllib

from django.conf import settings

import jinja2
from funfactory.utils import absolutify
from jingo import register

PARAGRAPH_RE = re.compile(r'(?:\r\n|\r|\n){2,}')

absolutify = register.function(absolutify)


@register.filter
def paragraphize(value):
    return jinja2.Markup(
            u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
                         for p in PARAGRAPH_RE.split(jinja2.escape(value))))


@register.inclusion_tag('phonebook/includes/photo.html')
@jinja2.contextfunction
def profile_photo(context, profile):
    user = context['request'].user
    me = bool(user == profile.user)
    cachebust = profile.photo and bool(user.pk == profile.user_id)
    return dict(
            image_url=profile.get_photo_url(cachebust=cachebust),
            show_gravatar_info=not profile.photo and me,
    )


@register.inclusion_tag('phonebook/includes/search_result.html')
@jinja2.contextfunction
def search_result(context, profile):
    d = dict(context.items())
    d.update(profile=profile)
    return d


def gravatar(
            email,
            default='%simg/unknown.png' % (settings.MEDIA_URL),
            size=175,
            rating='pg'):
    """Return the Gravatar URL for an email address."""

    return 'http://www.gravatar.com/avatar/%s?%s' % (
            hashlib.md5(email.lower()).hexdigest(),
            urllib.urlencode({
                'd': absolutify(default),
                's': str(size),
                'r': rating,
            })
    )
