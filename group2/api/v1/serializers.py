from rest_framework import serializers


class BlockSerializer(serializers.Serializer):
    username = serializers.CharField()

