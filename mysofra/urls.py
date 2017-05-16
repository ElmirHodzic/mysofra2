from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from mysofra import views

urlpatterns = [
    url(r'^products/$', views.ProductList.as_view()),
    url(r'^products/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view()),
    url(r'^mails/$', views.MailList.as_view()),
    url(r'^mails/(?P<pk>[0-9]+)/$', views.MailDetail.as_view()),
    url(r'^checkouts/new/$', views.new_checkout),
    url(r'^checkouts/(?P<transaction_id>[a-z0-9]+)/$', views.show_checkout),
    url(r'^checkouts/$', views.create_checkout),
]

urlpatterns = format_suffix_patterns(urlpatterns)