from django.conf.urls import url

from . import views

urlpatterns= [
    url(r'executeBot/$',views.executeBot,name='executeBot')
]