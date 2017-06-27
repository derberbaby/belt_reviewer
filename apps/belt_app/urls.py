from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^books/add$', views.create, name='create'),
    url(r'^add$', views.add, name='add'),
    url(r'^books$', views.main, name='main'),
    url(r'^books/(?P<book_id>\d+)$', views.book, name='book'),
    url(r'^review_book/(?P<book_id>\d+)$', views.review_book, name='review_book'),
    url(r'^fave/(?P<book_id>\d+)$', views.fave, name='fave'),
    url(r'^users/(?P<user_id>\d+)$', views.user, name='user'),
    url(r'^add_friend/(?P<friend_id>\d+)$', views.add_friend, name='add_friend'),
    url(r'^del_friend/(?P<friend_id>\d+)$', views.del_friend, name='del_friend'),
    url(r'^author/(?P<author_id>\d+)$', views.author, name='author'),
    url(r'^delete/(?P<review_id>\d+)$', views.delete, name='delete'),
    # url(r'^del_auth/(?P<author_id>\d+)/(?P<book_id>\d+)$', views.del_auth, name='del_auth'),
    url(r'^home$', views.home, name='home'),
    url(r'^logout$', views.logout, name='logout')
]
