# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('wan/sites', views.sites, name='sites'),
    path('wan/interfaces', views.interfaces, name='interfaces'),
    path('wan/applications', views.applications, name='applications'),
    path('wan/outburst', views.outburst, name='outburst'),
    path('wan/inburst', views.inburst, name='inburst'),
]
