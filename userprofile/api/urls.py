from django.urls import path

from . import views

app_name = 'api_userprofile'
urlpatterns = [
    path('getme/', views.GetMeApiView.as_view(), name='getme'),
    path('user-list/', views.UserListApiView.as_view(), name='list_user'),
    path('user/<int:id>/', views.UserDetailApiView.as_view(), name='detail_user'),
    path('signup/', views.SignUpApiView.as_view(), name='user_signup'),
    path('add-member/', views.AgenRegistUserApiView.as_view(), name='add_member'),
    path('limit/update/<uuid:id>/', views.UpdateLimitApiView.as_view(), name='update_limit'),
]