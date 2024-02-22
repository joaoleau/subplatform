from django.urls import path
from .views import (
    DashboardView,
    CreateArticleView,
    ListArticleView,
    DetailArticleView,
    MyArticlesView,
    UpdateArticleView
)

app_name = "writer"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="writer-dashboard"),
    path("article-create/", CreateArticleView.as_view(), name="article-create"),
    path("articles/", ListArticleView.as_view(), name="article-list"),
    path("article/<int:pk>/", DetailArticleView.as_view(), name="article-detail"),
    path("article/update/<int:pk>/", UpdateArticleView.as_view(), name="article-update"),
    path("my-articles/", MyArticlesView.as_view(), name="my-articles")
]
