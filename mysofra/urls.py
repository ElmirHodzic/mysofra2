from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from mysofra import views

urlpatterns = [
    url(r'^profiles/$', views.ProfileList.as_view()),
    url(r'^profiles/(?P<pk>[0-9]+)/$', views.ProfileDetail.as_view()),
    url(r'^products/$', views.ProductList.as_view()),
    url(r'^products/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view()),
    url(r'^categories/$', views.CategoryList.as_view()),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.CategoryDetail.as_view()),
    url(r'^mails/$', views.MailList.as_view()),
    url(r'^mails/(?P<pk>[0-9]+)/$', views.MailDetail.as_view()),
    url(r'^checkouts/new/(?P<pk>[0-9]+)/$', views.new_checkout),
    url(r'^checkouts/(?P<transaction_id>[a-z0-9]+)/$', views.show_checkout),
    url(r'^checkouts/$', views.create_checkout),
    url(r'^logintest/$', views.logintest),
]

urlpatterns = format_suffix_patterns(urlpatterns)
