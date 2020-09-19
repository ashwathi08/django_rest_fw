from django.urls import path,include
from profile_api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('hello-viewset',views.HelloViewset,basename='hello-viewset')
router.register('profile',views.UserProfileViewset)
router.register('login',views.LoginViewset,basename='login')
router.register('feed',views.ProfileFeedViewset)
urlpatterns=[
    path('home_api/',views.HelloApiView.as_view()),
    path('',include(router.urls))
]