from rest_framework import viewsets

from apps.communities.models import Community
from apps.communities.serializers import CommunitySerializerVersion1


class CommunityViewSetApiEventVersion1(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializerVersion1
