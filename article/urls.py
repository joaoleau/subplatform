from django.urls import path
from .views import (
    CreateArticleView,
    DetailArticleView,
    MyArticlesView,
    UpdateArticleView,
    DeleteArticleView,
    ListArticleView,
)

app_name = "article"

urlpatterns = [
    path("article/create/", CreateArticleView.as_view(), name="article-create"),
    path("article/<int:pk>/", DetailArticleView.as_view(), name="article-detail"),
    path("articles/", ListArticleView.as_view(), name="article-list"),
    path(
        "article/update/<int:pk>/", UpdateArticleView.as_view(), name="article-update"
    ),
    path(
        "article/delete/<int:pk>/", DeleteArticleView.as_view(), name="article-delete"
    ),
    path("article/me/", MyArticlesView.as_view(), name="my-articles"),
]
