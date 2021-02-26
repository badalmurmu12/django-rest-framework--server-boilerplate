from rest_framework.routers import SimpleRouter
from .views import  LoginInitiator, UsersViewSet, SignupViewSet
from django.urls import re_path, include, path
from django.conf.urls import url
from oauth2_provider import views

router = SimpleRouter()

router.register(r'users', UsersViewSet, basename='user')
urlpatterns = [
    re_path(r'^', include(router.urls)),
    url(r"^authorize/$", views.AuthorizationView.as_view(), name="authorize"),
    url(r"^token/$", views.TokenView.as_view(), name="token"),
    url(r"^revoke_token/$", views.RevokeTokenView.as_view(), name="revoke-token"),
    url(r"^introspect/$", views.IntrospectTokenView.as_view(), name="introspect"),
    path(r'logininitiator/', LoginInitiator.as_view()),
    path(r'signup/', SignupViewSet.as_view()),
]