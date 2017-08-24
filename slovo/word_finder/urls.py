from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    url('^main/$', views.main, name='main'),
    url('^compute/$', views.compute, name='compute'),
]
