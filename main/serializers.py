from rest_framework import serializers
from .models import *


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'title', )

    def to_representation(self, instance):
        representation = super(CategoryDetailSerializer, self).to_representation(instance)
        return representation

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('image', )

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'price', 'category', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        user = request.user.profile_master
        post = Post.objects.create(author=user, **validated_data)
        for image in images_data.getlist('images'):
            PostImage.objects.create(post=post, image=image)
        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            PostImage.objects.create(post=instance, image=image)
        return instance

    def to_representation(self, instance):
        representation = super(PostSerializer, self).to_representation(instance)
        action = self.context.get('action')
        reviews = ReviewSerializer(instance.reviews.all(), many=True).data
        likes = LikeSerializer(instance.likes.filter(like=True), many=True).data
        representation['author'] = instance.author.email
        representation['images'] = PostImageSerializer(instance.images.all(), many=True, context=self.context).data
        if action == 'list':
            representation['reviews'] = len(reviews)
            representation['likes'] = len(likes)
        if action == 'retrieve':
            representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
            representation['likes'] = LikeSerializer(instance.likes.filter(like=True), many=True).data
            representation['recommends'] = RecommendSerializer(Post.objects.filter(category__exact=instance.category)[:5],
                                                          many=True).data
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'post', 'text', )

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user.profile_customer
        review = Review.objects.create(user=user, **validated_data)
        return review

    def to_representation(self, instance):
        representation = super(ReviewSerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        return representation


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'description', 'category', )
