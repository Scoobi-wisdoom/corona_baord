from django.urls import path, re_path
from baseapp import views
from django.views.generic import TemplateView
from baseapp.sitemaps import sitemaps
from django.contrib.sitemaps import views as sitemap_views
from django.conf.urls.static import static

app_name = 'baseapp'

urlpatterns = [
    re_path(r'^robots\.txt$',
            TemplateView.as_view(template_name="others/robots.txt", content_type="text/plain"), name="robots"),
    path('a/sitemap.xml', sitemap_views.index, {'sitemaps': sitemaps, 'sitemap_url_name': 'baseapp:sitemaps'}),
    path('a/sitemap-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps},
            name='sitemaps'),
    re_path(r'^$', views.home, name='home'),
    re_path(r'^chart/$', views.chart, name='chart'),
    re_path(r'^news/$', views.news, name='news'),
    re_path(r'^add_post/$', views.add_post, name='add_post'),
    re_path(r'^update_youtube/$', views.update_youtube, name="update_youtube"),
    re_path(r'^update_bbc/$', views.update_bbc, name="update_bbc"),
    re_path(r'^update_country/$', views.update_country, name="update_country"),
]


from django.conf import settings

if settings.DEBUG:

    urlpatterns += [

        #
        # re_path(r'^b/admin/$', views.b_admin, name='b_admin'),
        # re_path(r'^b/admin/solo/$', views.b_admin_solo, name='b_admin_solo'),
        # re_path(r'^b/admin/group/$', views.b_admin_group, name='b_admin_group'),
        # re_path(r'^b/admin/member/$', views.b_admin_member, name='b_admin_member'),
        # re_path(r'^b/admin/group/edit/(?P<uuid>([0-9a-f]{32}))/$', views.b_admin_group_edit, name='b_admin_group_edit'),
        # re_path(r'^b/admin/solo/edit/(?P<uuid>([0-9a-f]{32}))/$', views.b_admin_solo_edit, name='b_admin_solo_edit'),
    ]