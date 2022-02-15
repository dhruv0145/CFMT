from django.urls import path

from . import views

app_name = 'myapp'
urlpatterns = [
    path('show/', views.show, name='show'),
    path('', views.companylistapi, name='index'),
    path('companylistapi/',views.companylistapi,name='companylistapi'),
    path('company/<str:pl>/',views.company,name='company'),
    path('round/<str:pl>/',views.round,name='round'),
    path('companybarapi/<str:pl>/',views.companybarapi,name='companybarapi'),
    path('state/',views.state, name='stateData'),
    path('stateapi/',views.statewise, name='stateApi'),
    path('category/',views.category, name='categoryData'),
    path('categoryapi/',views.categorywise, name='categoryApi'),
    path('crud/',views.crud,name='crud')
    ]