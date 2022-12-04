from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'home'

router = DefaultRouter()
router.register(r'contentviewset', views.ContentViewSet,basename="contentviewset")


urlpatterns = [

    path('', views.ContentClass.as_view(), name='content'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('content/', views.ContentClass.as_view(), name='content'),
    path('content/<id>', views.ContentDetailClass.as_view(), name='content_detail'),
    path('add_content/', views.AddContent.as_view(), name='add_content'),
    path('delete/<id>', views.DeleteContent.as_view(), name='delete_content'),

    path('get_content/', views.GetContent1.as_view(), name='get_content1'),
    path('get_content/<value1>&<value2>', views.GetContent2.as_view(), name='get_content2'),
    path('get_user/', views.GetUserInfo.as_view(), name='get_user'),
    path('delete_content/', views.DeleteContentAPI.as_view()),
    path('update_content/', views.UpdateContentAPI.as_view()),
    path('register/', views.RegisterAPI.as_view()),
    path('sort_content/', views.SortContentAPI.as_view()),
    path('search_content/', views.SearchContentAPI.as_view()),
] + router.urls