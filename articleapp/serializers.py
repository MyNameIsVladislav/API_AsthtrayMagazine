from rest_framework import serializers
from articleapp.models import ArticleModel, CommentsModel, ModelLikesArticle


class CommentsSerializer(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(slug_field='last_name', read_only=True)

    class Meta:
        model = CommentsModel
        fields = ('user_id', 'article_id', 'text')


class CommentCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=1)

    class Meta:
        model = CommentsModel
        fields = ('user_id', 'article_id', 'text')


class LikeCreateSerializer(CommentCreateSerializer):
    status = serializers.HiddenField(default=True)

    class Meta:
        model = ModelLikesArticle
        fields = ('user_id', 'article_id', 'status')


class ArticleSerializers(serializers.ModelSerializer):
    owner_id = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    genres_id = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    likes = serializers.IntegerField(min_value=0)

    class Meta:
        model = ArticleModel
        exclude = ('is_active', 'text', 'created_at', 'updated_at')


class ArticleDetailSerializer(ArticleSerializers):
    articleapp_commentsmodel = CommentsSerializer(read_only=True, many=True)

    class Meta:
        model = ArticleModel
        fields = '__all__'
