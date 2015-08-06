"""The URL patterns of the ahmia."""
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from ahmia.forms import WordsSearchForm
from ahmia.views import CustomSearchView
from haystack.views import search_view_factory

urlpatterns = patterns('',
    # Check is domain up.
    # domain:port/address/3g2upl4pq6kufc4m/up
    (r'^address/([a-z2-7]{16})/status', 'ahmia.views_online_test.onion_up'),
    # Edit information of a hidden service
    # domain:port/address/3g2upl4pq6kufc4m/edit
    (r'^address/([a-z2-7]{16})/edit', 'ahmia.views.onion_edit'),
    # Popularity of a hidden service
    (r'^address/([a-z2-7]{16})/popularity', 'ahmia.views.onion_popularity'),
    #/address/ API
    # domain:port/address/3g2upl4pq6kufc4m
    (r'^address/([a-z2-7]{16})', 'ahmia.views.single_onion'),
    # All domains that are online and are not banned
    (r'^address/online', 'ahmia.views.onions_online_txt'),
    # Invalid /address URL.
    (r'^address/(.+)', 'ahmia.views.onion_error'),
    # GET lists every known HS and POST adds a new HS.
    # domain:port/address/
    (r'^address/', 'ahmia.views.onion_list'),
    # Redirect link to hidden service
    (r'^redirect', 'ahmia.views.onion_redirect'),
    # Banned hidden services (MD5).
    # The plain texts list of onion URL.
    (r'^onions/', 'ahmia.views.onions_txt'),
    (r'^oniondomains\.txt$', 'ahmia.views.onions_txt'),
    # Add domain form.
    (r'^add/', 'ahmia.views.add'), #domain:port/add
    (r'^search/', 'ahmia.views_search.results'), # results
    (r'^$', 'ahmia.views_search.default') #domain:port
)

# Elasticsearch API
urlpatterns += patterns('',
    (r'^elasticsearch/', 'ahmia.views_search.proxy'),
)

# Haystack based search
urlpatterns += patterns('',
    # The full text search page.
    (r'^search/autocomplete', 'ahmia.views_search.autocomplete'),
    url(r'^search/', search_view_factory(
            view_class=CustomSearchView,
            form_class=WordsSearchForm
        ), name='haystack_search'),
)

# Stats views
urlpatterns += patterns('',
    # Stats
    (r'^stats/viewer', 'ahmia.views_stats.statsviewer'),
    (r'^stats/popularity', 'ahmia.views_stats.stats'),
    (r'^stats/tor2web', 'ahmia.views_stats.tor2web'),
    (r'^stats/history', 'ahmia.views_stats.history'),
    (r'^stats/traffic', 'ahmia.views_stats.trafficviewer'),
    (r'^stats/services', 'ahmia.views_stats.services'),
    (r'^stats/onionsovertime', 'ahmia.views_stats.onionsovertime'),
)

# Rule views
urlpatterns += patterns('',
    # Login and logout.
    (r'^rule/login/', 'ahmia.views_admin.login'),
    (r'^rule/logout/', 'ahmia.views_admin.logout'),
    # Rule content.
    (r'^rule/$', 'ahmia.views_admin.rule'),
)


# From views_static
urlpatterns += patterns('',
    # Blacklist MD5
    (r'^blacklist/banned', 'ahmia.views.banned'),
    # Blacklist reporting
    (r'^blacklist/report', 'ahmia.views.blacklist_report'),
    # Banned services
    (r'^blacklist', 'ahmia.views.blacklist'),
    # legalese
    (r'^legal', 'ahmia.views_static.legal'),
    # documentation/indexing
    (r'^documentation/indexing/', 'ahmia.views_static.indexing'),
    # Documentation - create hidden service description to hidden services.
    (r'^documentation/createHsDescription/',
    'ahmia.views_static.create_description'),
    # Documentation - description proposal to hidden services.
    (r'^documentation/descriptionProposal/',
    'ahmia.views_static.description_proposal'),
    # Documentation page.
    (r'^documentation/', 'ahmia.views_static.documentation'),
    # Information about ahmia.
    (r'^about/', 'ahmia.views_static.about'),
    # Show visitor's IP address.
    (r'^IP/', 'ahmia.views_static.show_ip'),
)

# robots.txt file
urlpatterns += patterns('',
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
    content_type='text/plain')),
)

# Yacy wrapping
urlpatterns += patterns('',
    # Full text search using YaCy wrapper.
    # Load under /static/
    (r'^yacy/(.*)', 'ahmia.views_search.yacy_static'),
    (r'^env/(.*)', 'ahmia.views_search.yacy_static'),
    (r'^currentyacypeer/(.*)', 'ahmia.views_search.yacy_static'),
    (r'^portalsearch/(.*)', 'ahmia.views_search.yacy_static'),
    (r'^jquery/(.*)', 'ahmia.views_search.yacy_static'),
    (r'^js/(.*)', 'ahmia.views_search.yacy_static'),
    # Use the wrapper
    (r'^api/(.*)', 'ahmia.views_search.yacy_connection'),
    (r'^yacysearch.rss(.*)', 'ahmia.views_search.yacy_connection'),
    (r'^yacysearch.html(.*)', 'ahmia.views_search.yacy_connection'),
    (r'^suggest.json(.*)', 'ahmia.views_search.yacy_connection'),
    (r'^cytag.png(.*)', 'ahmia.views_search.yacy_connection'),
    (r'^index.html(.*)', 'ahmia.views_search.yacy_connection'),
    (r'^ViewImage.png(.*)', 'ahmia.views_search.yacy_connection'),
)

# DEPRECATED ROUTES
urlpatterns += patterns('',
    (r'^policy/', 'ahmia.views_legacy_redirect.policy'),
    (r'^disclaimer/', 'ahmia.views_legacy_redirect.disclaimer'),
    (r'^banned/', 'ahmia.views_legacy_redirect.blacklist'),
    (r'^bannedMD5\.txt$', 'ahmia.views_legacy_redirect.banned')
)

#media files: CSS, JavaScript, images
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    )
