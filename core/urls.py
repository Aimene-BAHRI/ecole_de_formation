# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

import notifications.urls

urlpatterns = [
    # path('admin/', admin.site.urls),          # Django admin route
    path("accounts/", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")) ,            # UI Kits Html files
    
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)