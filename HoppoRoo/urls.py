"""HoppoRoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from HLS import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home$', views.home),
    url(r'^quizview$', views.quiz_view),
    url(r'^loadquiz$', views.load_quiz),
    url(r'^createquiz$', views.create_quiz),
    url(r'^api/v1/quizdata', views.quiz_data),
    url(r'^create_quiz$', views.create_quiz),
    url(r'^create_quiz_ap$', views.create_quiz_ap),
    url(r'^api/v1/data$', views.data_access_point),

]
