from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^users/login', 'mysite.cs169proj1.login'),
    #url(r'^users/add', 'mysite.cs169proj1.add'),
    #url(r'^TESTAPI/resetFixture', 'mysite.cs169proj1.TESTAPI'),
    url(r'^users/login','cs169proj1.views.login'),
    url(r'^users/add', 'cs169proj1.views.add'),
    url(r'^TESTAPI/resetFixture', 'cs169proj1.views.resetFixture'),
    url(r'^TESTAPI/unitTests', 'cs169proj1.views.unitTests'),
    url(r'^$', 'cs169proj1.views.users'),
    url(r'^client.js', 'cs169proj1.views.clientjs'),
    url(r'^client.css','cs169proj1.views.clientcss'),
    url(r'^login.css', 'cs169proj1.views.logincss'),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)
