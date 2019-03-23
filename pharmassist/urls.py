"""pharmassist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import views

from microblog import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('all-refills/', views.view_all_refills, name="all_refills"),
    path('update-refill/<refill_id>/', views.update_refill),
    path('delete-refill/<refill_id>/', views.delete_refill),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('new-med/', views.new_med, name='newmedform'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
]

# NOTE: To get media working, we need to do something like this. See
# also the end of the settings.py file.
from django.conf.urls.static import static
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
