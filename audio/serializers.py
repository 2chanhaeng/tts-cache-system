from rest_framework import serializers
from .models import Project, Audio, Sentence
from .utils.audio_converter import separate_text_by_sentence


class ProjectCreateSerializer(serializers.ModelSerializer):
    text = serializers.CharField()

    class Meta:
        model = Project
        fields = ("project_title", "text")

    def create(self, validated_data: dict[str, str]):
        title = validated_data.get("project_title")
        project = Project.objects.create(project_title=title)
        text = validated_data.get("text")
        sentences = separate_text_by_sentence(text)
        for index, sentence_text in enumerate(sentences):
            sentence, _ = Sentence.objects.get_or_create(text=sentence_text)
            Audio.objects.create(
                project_id=project,
                index=index,
                sentence=sentence,
            )
        return project


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ("id", "text", "speed", "index")

    def update(self, instance, validated_data):
        if instance.text != validated_data.get("text"):
            sentence, _ = Sentence.objects.get_or_create(
                text=validated_data.get("text")
            )
            instance.sentences = sentence
        instance.speed = validated_data.get("speed")
        instance.save()
        return instance
