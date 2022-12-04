from zakat_posts.models import ZakatPosts
from rest_framework import viewsets
from zakat_posts.api.serializers import ZakatPostsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



class ZakatPostsViewSet(viewsets.ModelViewSet):
  queryset = ZakatPosts.objects.all()
  serializer_class = ZakatPostsSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)