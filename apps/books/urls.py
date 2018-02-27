from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.login_page),
	url(r'^register$', views.register),
	url(r'^users/(?P<id>\d+)$', views.users),
	url(r'^users/(?P<id>\d+)/edit$', views.register),
	url(r'books$', views.books_page),
	url(r'^books/(?P<id>\d+)$', views.each_book_page),
	url(r'^books/add$', views.add_book_page),
	url(r'books/(?P<id>\d+)/review$', views.add_review),
	url(r'^login$', views.login),
	url(r'logout$', views.log_out)
]
