"""jobshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from frontend import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='../templates/main/login.html'), name='login'),
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
    path('home', views.textile_home, name='home'),

    ## common pages
    path('test/', views.test),
    path('nav/', views.nav),
    path('footer/', views.footer),
    path('topbar/', views.topbar),
    path('board/', include('board.urls'), name='board'),
    path('common/', include('common.urls')),

    ## textile urls
    path('textile/home', views.textile_home, name='textile.home'),
    path('textile/board/', views.board),
    path('textile/company/', include('company.urls'), name='company'),
    path('textile/schedule/', include('schedule.urls'), name='schedule_'),
    path('textile/recommend/', include('recommend.urls')),
    path('textile/order/', include('order.urls'), name='order'),

    ## algorithm test urls
    path('algorithm/home', views.algorithm_home, name='algorithm.home'),
    path('algorithm/schedule/', include('schedule.urls'), name='algorithm'),

]
# 파일 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
