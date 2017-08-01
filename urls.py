from django.conf.urls import url
from django.conf.urls.defaults import *
from myapp.views import signup_view, login_view, feed_view, post_view, like_view, comment_view, logout_view, search_view, upvoting_view, product_view

urlpatterns = [
    url('post/', post_view),
    url('feed/', feed_view),
    url('like/', like_view),
    url('comment/', comment_view),
    url('login/', login_view),
    url('', signup_view),
    url('logout/', logout_view),
    url('upvoting/', upvoting_view),
    url('products/',product_view),
    url('search/',search_view)
]