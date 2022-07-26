from django.core.mail import send_mail
from rest_framework import serializers

from applications.product.models import Category, Product, Image, Rating, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        # representation['hello'] = 'hello john'
        if not instance.parent:
            representation.pop('parent')
        return representation


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')


    class Meta:
        model = Comment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    images = ImageSerializer(many=True,read_only=True)
    comments = CommentSerializer(many=True,read_only=True)


    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        product = Product.objects.create(**validated_data)
        print(images)

        for image in images.getlist('images'):
            Image.objects.create(product=product, image=image)

        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.likes.filter(like=True).count())
        representation['likes'] = instance.likes.filter(like=True).count()
        rating_result = 0
        for rating in instance.ratings.all():
            rating_result += int(rating.rating)
        try:
            representation['rating'] = rating_result / instance.ratings.all().count()
        except ZeroDivisionError:
            # representation['rating'] = 0
            pass
        representation['best name '] = 'John' #Пример


        #TODO: Отображать рейтинг (средний)
        return representation



class RatingSerializer(serializers.ModelSerializer):


    class Meta:
        model = Rating
        fields = ['rating']

    rating = serializers.IntegerField(required=True,min_value=1,max_value=5)



# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#
#     def validate_email(self, email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('Пользователь не зарегистрирован')
#         return email
#
#     def send_code(self):
#         email = self.validated_data.get('email')
#         user = User.objects.get(email=email)
#         user.generate_activation_code()
#         send_mail(
#             'Восстановление пароля',
#             f'Ваш код подтверждения: {user.activation_code}',
#             'test@gmail.com',
#             [email]
#         )
#
#
# class ForgotPasswordCompleteSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     code = serializers.CharField(min_length=8, max_length=8, required=True)
#     password = serializers.CharField(required=True)
#     password_confirm = serializers.CharField(required=True)
#
#     def validate_email(self, email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('Пользователь не зарегистрирован')
#         return email

    # def validate_code(self, code):
    #     if not User.objects.filter(activation_code=code).exists():
    #         raise serializers.ValidationError('Пользователь не зарегистрирован')
        # return code
    #
    # def validate(self, attrs):
    #     pass1 = attrs.get('password')
    #     pass2 = attrs.get('password_confirm')
    #     if pass1 != pass2:
    #         raise serializers.ValidationError('Пароли не совпадают')
    #     return attrs
    #
    # def set_new_pass(self):
    #     email = self.validated_data.get('email')
    #     password = self.validated_data.get('password')
    #     user = User.objects.get(email=email)
    #     user.set_password(password)
    #     user.activation_code = ''
    #     user.save()