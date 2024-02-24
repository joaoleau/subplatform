from django.urls import path
from .views import (
    DashboardView,
    CreateArticleView,
    DetailArticleView,
    MyArticlesView,
    UpdateArticleView,
    DeleteArticleView,
)

app_name = "article"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="writer-dashboard"),
    path("article/create/", CreateArticleView.as_view(), name="article-create"),
    path("article/<int:pk>/", DetailArticleView.as_view(), name="article-detail"),
    path(
        "article/update/<int:pk>/", UpdateArticleView.as_view(), name="article-update"
    ),
    path(
        "article/delete/<int:pk>/", DeleteArticleView.as_view(), name="article-delete"
    ),
    path("article/me/", MyArticlesView.as_view(), name="my-articles"),
]
