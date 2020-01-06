from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    #summary = serializers.TextField(max_length=1000)
