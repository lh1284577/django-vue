from rest_framework import serializers
from yunwei.models import AESSLIST



class AESSLISTSerializer(serializers.ModelSerializer):
	class Meta:
		model = AESSLIST
		fields = '__all__'
