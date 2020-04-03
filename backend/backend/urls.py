"""backend URL Configuration

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
# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('wikingram/', views.query, name="WikiNgramViewer"),
    path('similarity/', views.clustersearch, name="SimilaritySearch"),
    path('datasets/', views.datasets, name="Datasets"),
    path('landing/', views.landing, name="Landing"),
	path("json_result", views.json_result, name="json_result"),
    path("json_result_plot", views.json_result_plot, name="json_result_plot"),
    path("wiki-instruction", views.wiki_instruction, name="wiki-instruction")
]
