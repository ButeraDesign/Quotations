from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^register$', views.register),
	url(r'^quotes$', views.quotes),
	url(r'^userQuotes/(?P<user_id>\d+)$', views.userQuotes),
	url(r'^createQuote$', views.createQuote),
	url(r'^addFavorite/(?P<fav_id>\d+)/(?P<user_id>\d+)$', views.addFavorite),
	url(r'^delFavorite/(?P<fav_id>\d+)/(?P<user_id>\d+)$', views.delFavorite),
]
