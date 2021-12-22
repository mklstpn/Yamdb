from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User, UserRole


class UserAdminSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=UserRole.CHOICES, default=UserRole.USER)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Using me as a username is forbidden')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=10, required=True)


class ReviewSerializer(serializers.ModelSerializer):
    title = SlugRelatedField(slug_field='name', read_only=True)
    author = SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())

    def validate(self, data):
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        title = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=request.user, title=title).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв!')
        return data

    class Meta:

        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=('name', 'slug'),
                message='Такая категория уже существует'
            )
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']
        validators = [
            UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=('name', 'slug'),
                message='Такой жанр уже существует'
            )
        ]


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerCreate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
        required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        required=False, many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
