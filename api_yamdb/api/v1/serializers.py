import datetime as dt
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'category',
            'genre',
            'description',
        )

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value < year):
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'category',
            'genre',
            'description',
        )


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Not a valid username.',
        )
    ])

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Using "me" as a username is forbidden.'
            )
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'A user with that username already exists.'
            )
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'A user with that email already exists.'
            )
        return data


class JwtTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True, validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='A user with that username is not found.',
        )
    ])


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'score', 'text', 'pub_date', 'author',)
        read_only_fields = ('id', 'pub_date', 'author',)

    def validate(self, data):
        is_review_exist = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs['title_id']
        ).exists()

        if self.context['request'].method == 'POST' and is_review_exist:
            raise serializers.ValidationError(
                'You cannot add review for the same title twice!')

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'pub_date', 'author',)
        read_only_fields = ('id', 'pub_date', 'author',)
