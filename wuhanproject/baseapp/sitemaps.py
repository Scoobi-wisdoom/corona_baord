from django.contrib.sitemaps import Sitemap
from django.core.cache import cache
from django.core.paginator import Paginator
from django.urls import reverse
from forum.models import *


class HomeSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    protocol = "https"

    def items(self):
        return ['baseapp:home']

    def location(self, item):
        return reverse(item)


class PostListSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    protocol = "https"

    def items(self):
        return ['forum:post_list']

    def location(self, item):
        return reverse(item)


class PostDetailSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = "https"

    def items(self):
        return Post.objects.all().order_by('-date_published')

    def lastmod(self, obj):
        return obj.date_updated


class ChartSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    protocol = "https"

    def items(self):
        return ['baseapp:chart']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'home': HomeSitemap,
    'post_list': PostListSitemap,
    'post_detail': PostDetailSitemap,
    'chart': ChartSitemap
}
