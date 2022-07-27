from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("Signup", views.SignupModelViewSet, basename="Signup")
# router.register("User_Todo", views.TodoModelViewSet, basename="User_Todo")
router.register("Login", views.LoginModelViewSet, basename="Login")
router.register("Favtodo", views.TodoFavModelViewSet, basename="User_Favtodo")
router.register("IsDoneTodo", views.TodoisdoneModelViewSet, basename="User_ComplatedTodo")
#router.register("Create_Todo", views.TodoListCreate, basename="Create_Todo")
router.register("Todo", views.Todo_Update_Retrieve_Destory, basename="Update_Todo")
router.register("Profile", views.UserProfile, basename="User_Profile")


urlpatterns = [
    path("", include(router.urls)),
    # path("create_todo/", views.TodoListCreate.as_view()),
    # path("change_todo/<int:pk>/", views.Todo_Update_Retrieve_Destory.as_view()),
    # path("add_or_remove_todo_done/<int:pk>/", views.User_isdone_Todo.as_view()),
    # path("add_or_remove_fav_todo/<int:pk>/", views.User_fav_Todo.as_view()),


]
