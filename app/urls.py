"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from app.core import urls as core_urls
from app.account import urls as account_urls
from app.task import urls as task_urls
from app.route import urls as route_urls
from app.notification import urls as notification_urls
from app.wiki import urls as wiki_urls
from app.partner import urls as partner_urls
from app.client import urls as client_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ajaximage/', include('ajaximage.urls')),
    url(r'^ajax-upload/', include('ajax_upload.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    # url(r'^tagging/', include('tagging_autosuggest.urls')),
    # url(r'^tagging/', include('tagging.urls', namespace='tagging')),
    url(r'^select2/', include('django_select2.urls')),

    url(r'^$', 'app.core.views.front_page', name='front_page'),
    url(r'^accounts/', include(account_urls, namespace='account')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/', include(task_urls, namespace='task')),
    url(r'^routes/', include(route_urls, namespace='route')),
    url(r'^notifications/', include(notification_urls, namespace='notification')),
    url(r'^wiki/', include(wiki_urls, namespace='wiki')),
    url(r'^partners/', include(partner_urls, namespace='partner')),
    url(r'^clients/', include(client_urls, namespace='client')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
