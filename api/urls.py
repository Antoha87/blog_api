from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from blog.views import PostViewSet, LikeView


Router = routers.DefaultRouter()
Router.register('post', PostViewSet)

urlpatterns = [
    path('blog/', include(Router.urls)),
    path('blog/post/<str:slug>/like', LikeView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path('docs/', include_docs_urls(title='My API'))
]