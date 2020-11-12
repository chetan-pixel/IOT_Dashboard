"""ajax_showing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from . import views
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.signIn),
    url(r'^postsign/',views.postsign),
    url(r'^logout/',views.logout,name="log"),
    url(r'^signup/',views.signUp,name='signup'),
    url(r'^postsignup/',views.postsignup,name='postsignup'),
    # url(r'^cls/',views.check_load_save,name='cls'),
    # url(r'^sd/',views.show_devices,name='showdevices'),
    # url(r'^post_device/',views.post_device,name='showdevices'),



    url(r'^listdevices/',views.list_devices,name='listdevices'),
    url(r'^device_data/',views.device_data,name='device_data'),

    url('ajax_index', views.ajax_index, name = "ajax_index"),
    url('ajax_update/', views.ajax_update , name='ajax_update'),
    path('index_login/', TemplateView.as_view(template_name="index_login.html")),
    path('index_dashboard/', TemplateView.as_view(template_name="index_dashboard.html"), name="index_dashboard"),
    path('latest_data/', views.save_latest_data, name="noname"),
    url(r'^api/', views.filter_data, name="api"),
]

