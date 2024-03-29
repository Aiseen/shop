from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from applications.account.serializers import ForgotPasswordCompleteSerializer
from applications.product.models import Category, Product, Like, Rating, Comment
from applications.product.permissions import CustomIsAdmin
from applications.product.serializers import CategorySerializer, ProductSerializer, RatingSerializer, CommentSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000




class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LargeResultsSetPagination
    # permission_classes = [IsAdminUser]
    permission_classes = [CustomIsAdmin]


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter] #аналог def_queryset
    filterset_fields = ['category','owner'] #аналог def_queryset
    ordering_fields = ['name', 'id']
    search_fields = ['name', 'description']



    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #....product/1/like/
    @action(methods=['POST'], detail=True)
    def like(self,request,pk,*args,**kwargs):
     try:

        like_object, _ =  Like.objects.get_or_create(owner=request.user,product_id=pk)
        like_object.like = not like_object.like
        like_object.save()
        status = 'liked'

        if like_object.like:
            return Response({'status': status})
        status = 'unliked'
        return Response({'status': status})
     except:
         return Response('Нет такого продукта')

    @action(methods=['POST'], detail=True)
    def rating(self,request,pk,*args,**kwargs):
        serializers = RatingSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(product_id=pk,
                                              owner=request.user)

        # obj.rating = request.data['rating']
        obj.save()
        return Response(request.data,status=201)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [IsAuthenticated]
        elif self.action == 'like' or self.action == 'rating':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]

        return [p() for p in permissions]



class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)













#
# class ForgotPasswordView(APIView):
#     def post(self, request):
#         data = request.data
#         serializer = ForgotPasswordSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.send_code()
#         return Response('Вам отправлено письмо для восстановления пароля')
#
#
# class ForgotPasswordComplete(APIView):
#     def post(self, request):
#         data = request.data
#         serializer = ForgotPasswordCompleteSerializer(data=data)

    #за отображение
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #
    #     filter_category = self.request.query_params.get('category')
    #
    #     if filter_category:
    #         queryset = queryset.filter(category=filter_category)
    #
    #         return queryset[0:2]








#Неправильно
# class CategoryView(ViewSet):
#     def list(self,request):
#         queryset = Category.objects.all()
#         serializer = CategorySerializer(queryset,many=True)
#         return Response(serializer.data)


    # def create(self,request):
    #     serializer = CategorySerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=201)
    #     return Response(serializer.errors,status=400)
