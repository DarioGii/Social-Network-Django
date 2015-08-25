from rest_framework import serializers
from social.models import Message


class MessageSerializer(serializers.ModelSerializer):

	""" Below are the chosen fields in the Message model for serialization.
	These will be used to create the json object displayed in the API page """

	class Meta:
		model = Message
		fields = ('pk', 'author', 'recip', 'private', 'time', 'message')