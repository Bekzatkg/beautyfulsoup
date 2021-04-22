from rest_framework import generics, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import Category, Post, Review, Like, Favorite
from .serializers import CategoryListSerializer, PostSerializer, ReviewSerializer, CategoryDetailSerializer, FavoriteSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .permissions import IsAuthorPostPermission, IsMasterPermission, IsCustomerPermission, IsAuthorReviewPermission
from django_filters.rest_framework import DjangoFilterBackend


class PaginationPost(PageNumberPagination):
    page_size = 5


class PaginationReview(PageNumberPagination):
    page_size = 10


class PermissionMixinPost:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsMasterPermission, ]
        elif self.action in ['update', 'partial_update', 'delete']:
            permissions = [IsAuthorPostPermission, ]
        else:
            permissions = [AllowAny, ]
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class PermissionMixinReview:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsCustomerPermission, ]
        elif self.action in ['update', 'partial_update', 'delete']:
            permissions = [IsAuthorReviewPermission, ]
        else:
            permissions = [AllowAny, ]
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny, ]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class PostViewSet(PermissionMixinPost, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PaginationPost
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', ]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        obj, created = Like.objects.get_or_create(user=request.user.profile_customer, post=post)
        if not created:
            obj.like = not obj.like
            obj.save()
        liked_or_unliked = 'liked' if obj.like else 'unliked'
        return Response(f'Successfully {liked_or_unliked} posts', status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        post = self.get_object()
        obj, created = Favorite.objects.get_or_create(user=request.user.profile_customer, post=post)
        if not created:
            obj.favorite = not obj.favorite
            obj.save()
        added_removed = 'added' if obj.favorite else 'removed'
        return Response(f'Successfully {added_removed} favorite', status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(PermissionMixinReview, viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PaginationReview


class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        qs = self.request.user.profile_customer
        queryset = Favorite.objects.filter(user=qs, favorite=True)
        return queryset
