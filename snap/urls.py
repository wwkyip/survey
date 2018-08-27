#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 10:41:54 2018

@author: winnyyip
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addratings',views.addratings, name='addratings'),
    path('alltrend',views.alltrend,name='alltrend'),
    path('trend',views.trend,name='trend'),
]