from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Project, Audio
from .serializers import ProjectCreateSerializer, AudioSerializer
from .utils.audio_converter import get_file_path


class AudioPagination(PageNumberPagination):
    page_size = 10


class ProjectCreateView(APIView):
    def post(self, request: Request) -> Response:
        """
        POST /api/v1/project/
        Create project.
        """
        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project: Project = serializer.save()
        audio_list = project.audio_set.all().order_by("index")
        return Response(AudioSerializer(audio_list, many=True).data)


class ProjectView(APIView):
    def get(self, request: Request, project_pk: int) -> Response:
        """
        GET /api/v1/project/<project_pk>/
        Get project from pk.
        """
        project = get_object_or_404(Project, pk=project_pk)
        audio = project.audio_set.all().order_by("index")
        # paginate
        paginator = AudioPagination()
        result_page = paginator.paginate_queryset(audio, request)
        return paginator.get_paginated_response(
            AudioSerializer(result_page, many=True).data
        )


class AudioView(APIView):
    def get(self, request: Request, audio_pk: int) -> Response:
        """
        GET /api/v1/audio/<audio_pk>/
        Get audio from pk.
        """
        audio = get_object_or_404(Audio, pk=audio_pk)
        return Response(AudioSerializer(audio).data)

    def put(self, request: Request, audio_pk: int) -> Response:
        """
        PUT /api/v1/audio/<audio_pk>/
        Update audio from pk.
        """
        audio = get_object_or_404(Audio, pk=audio_pk)
        serializer = AudioSerializer(audio, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request: Request, audio_pk: int) -> Response:
        """
        DELETE /api/v1/audio/<audio_pk>/
        Delete audio from pk.
        """
        audio = get_object_or_404(Audio, pk=audio_pk)
        index = audio.index
        project: Project = audio.project_id
        audio.delete()
        # update index
        audio_list: list[Audio] = project.audio_set.filter(index__gt=index,).order_by(
            "index",
        )
        for index, audio in enumerate(audio_list, start=index):
            audio.index = index
            audio.save()
        return Response(status=204)


class AudioDownloadView(APIView):
    def get(self, request: Request, audio_pk: int) -> Response:
        """
        GET /api/v1/audio/<audio_pk>/download/
        Download audio from pk.
        """
        audio = get_object_or_404(Audio, pk=audio_pk)
        file_path = get_file_path(audio.text)
        if not file_path.exists():
            raise NotFound("File not found.")
        ext = file_path.suffix.replace(".", "")
        file_name = f"{audio.text}.{ext}"
        with open(file_path, "rb") as file:
            response = Response(file)
        response["Content-Type"] = f"audio/{ext}"
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        return response
