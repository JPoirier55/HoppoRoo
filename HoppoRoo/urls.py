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
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^auth/$', views.auth_view),
    url(r'^home/$', views.home),
    url(r'^$', views.home),
    url(r'^quizview$', views.quiz_view),
    url(r'^quizzes$', views.quizzes_home),
    url(r'^quizzes/load_quiz$', views.load_quiz),
    url(r'^quizzes/create_quiz$', views.create_quiz),
    url(r'^quizzes/create_quiz/build$', views.build_quiz),
    url(r'^quizzes/recent_quizzes$', views.create_quiz),
    url(r'^students$', views.students),
    url(r'^students/add_new$', views.students_add),
    url(r'^results$', views.results),
    url(r'^help', views.help),
    url(r'^pdf_view$', views.pdf_view),
    url(r'^pdf_upload$', views.pdf_upload),
    url(r'^testing$', views.test_page),
    url(r'^choose_quiz$', views.choose_quiz),
    url(r'^question_view$', views.question_view),

    # ----------API urls----------------
    url(r'^api/v1/create_quiz_ap$', views.create_quiz_ap),
    url(r'^api/v1/data$', views.data_access_point),
    url(r'^api/v1/quizdata$', views.quiz_data),
    url(r'^api/v1/upload$', views.upload_file),
    url(r'^api/v1/delete$', views.delete_file),
    url(r'^api/v1/results_data$', views.result_post_point),
    url(r'^api/v1/quiz_data$', views.serve_quiz),
    url(r'^api/v1/add_student_device$', views.add_student_device),
    url(r'^api/v1/export$', views.export_xlsx),
]


# url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
# url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
# url(r'^accounts/auth/$', views.auth_view),
# url(r'^accounts/invalid/$', views.invalid_view),