from django.conf.urls import patterns, url
from social import views


urlpatterns = patterns('',
    # main page
    url(r'^$', views.index, name='index'),
    # signup page
    url(r'^signup/$', views.signup, name='signup'),
    # register new user
    url(r'^register/$', views.register, name='register'),
    # login page
    url(r'^login/$', views.login, name='login'),
    # logout page
    url(r'^logout/$', views.logout, name='logout'),
    # members page
    url(r'^members/$', views.members, name='members'),
    # friends page
    url(r'^friends/$', views.friends, name='friends'),
    # user profile edit page
    url(r'^profile/$', views.profile, name='profile'),
    # Ajax: check if user exists
    url(r'^checkuser/$', views.checkuser, name='checkuser'),
    # messages page
    url(r'^messages/$', views.messages, name='messages'),
    #APIs
    url(r'^api/$', views.MessageCollection.as_view()),
    url(r'^api/(?P<pk>\d+)/$', views.MessageDetail.as_view()),
)