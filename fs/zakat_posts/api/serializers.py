from zakat_posts.models import ZakatPosts
from rest_framework import serializers

class ZakatPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZakatPosts
        fields = '__all__'
        