from django.urls import path
from .views import ProjectCreateView, ProjectView, AudioView

urlpatterns = [
    path("project/", ProjectCreateView.as_view()),
    path("project/<int:project_pk>/", ProjectView.as_view()),
    path("audio/<int:audio_pk>/", AudioView.as_view()),
    path("audio/<int:audio_pk>/download", AudioView.as_view()),
]
