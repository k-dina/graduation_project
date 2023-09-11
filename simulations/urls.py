from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="simulations"),
    path("userspace", views.userspace, name="userspace"),
    path("newsimulation", views.newsimulation, name="newsimulation"),
    path("view_simulation/<str:id>/", views.view_simulation, name="view_simulation"),
    path("view_saved_simulation/<str:simulation_id>/", views.view_saved_simulation, name="view_saved_simulation"),
    path("get_snapshots/<str:id>/<int:step>/", views.get_snapshots, name="get_snapshots"),
    path("resume_simulation/<str:id>/<int:step>/", views.resume_simulation, name="resume_simulation"),
    path("drop_simulation_view/<str:simulation_id>/", views.drop_simulation_view, name="drop_simulation"),
    path("name_simulation_view/", views.name_simulation_view, name="name_simulation_view"),
    path("saved_simulations/", views.saved_simulations, name="saved_simulations"),
    path("options/<str:simulation_id>/", views.options_view, name="options"),
    path("rename_simulation/<str:simulation_id>/", views.rename_simulation_view, name="rename_simulation"),
    path("save_simulation_view/<str:simulation_id>/", views.save_simulation_view, name="save_simulation_view"),
]
