"""MINIPROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.i18n import JavaScriptCatalog
from django.contrib import admin
from django.urls import path
from fileupload.views import text_paste_view
from fileupload.views import welcome_view
from fileupload.views import analysis_view,speech
from employee.views import register_view,login_request,profile_view,dashboard_view,schedule_view,scheduler_view,logout_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
urlpatterns = [
    path('register/', register_view, name='register_view'),
    path('login/', login_request, name='login_view'),
    path('admin/', admin.site.urls),
    path('welcome/',welcome_view),
    path('upload/<int:eid>/<int:mid>/',text_paste_view),
    path('analysis/<int:eid>/<int:mid>/',analysis_view),
    path('profile/<int:id>/',profile_view),
    path('dashboard/<int:id>/',dashboard_view),
    path('schedule/<int:id>/',schedule_view),
    path('scheduler/<int:id>/',scheduler_view),
    path('speech/<int:eid>/<int:mid>/',speech),
    path('jsi18',JavaScriptCatalog.as_view(),name='js-catlog'),
    path('logout/',logout_view),
]

# urlpatterns += staticfiles_urlpatterns()

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
