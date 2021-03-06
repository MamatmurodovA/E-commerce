from django.shortcuts import get_object_or_404, Http404
from django.contrib.auth.models import User
from rest_framework import generics, filters, views, response, permissions, status
import django_filters

from apps.app import models as app_models
from apps.store import models as store_models
from apps.restful import serializers as restful_serializer
from apps.restful import filters as restful_filters
from apps.restful import permissions as restful_permissions
from apps.restful.pagination import WithTotalPagesCountPagination


class CategoryListView(generics.ListAPIView):
    queryset = app_models.Category.objects.filter(parent__isnull=True).order_by('-pk')
    serializer_class = restful_serializer.CategorySerializer
    search_fields = ['title', ]
    filter_fields = ['title', ]


class CategoryDetailView(generics.RetrieveAPIView):
    serializer_class = restful_serializer.CategorySerializer
    lookup_url_kwarg = 'slug'

    def get_object(self):
        return get_object_or_404(app_models.Category, **{'slug': self.kwargs.get('slug')})


class CategoryTreeView(views.APIView):

    def get(self, request, *args, **kwargs):
        resp = {}
        print(request)
        print('ID: ' + self.kwargs.get('slug'))
        if self.kwargs.get('slug') == 'all':
            resp['title'] = 'Барча маҳсулотлар'
            resp['id'] = 'all'
            resp['slug'] = 'all'
            return response.Response(resp)
        obj = get_object_or_404(app_models.Category, **{'slug': self.kwargs.get('slug')})
        if obj.parent:
            resp['title'] = obj.parent.title
            resp['id'] = obj.parent.id
            resp['slug'] = obj.parent.slug
            resp['child'] = {}
            resp['child']['title'] = obj.title
            resp['child']['id'] = obj.id
            resp['child']['slug'] = obj.slug
        else:
            resp['title'] = obj.title
            resp['id'] = obj.id
            resp['slug'] = obj.slug
        return response.Response(resp)


class BrandListView(generics.ListAPIView):
    queryset = app_models.Brand.objects.all()
    serializer_class = restful_serializer.BrandSerializer
    search_fields = ['title', 'category__title', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'cat' in self.request.GET:
            cat = self.request.GET['cat']
            category = app_models.Category.objects.get(pk=cat)
            cats = [cat]
            if category.children:
                for child_cat in category.children.all():
                    cats.append(child_cat.pk)
            queryset = queryset.filter(category_id__in=cats)
        return queryset


class ProductListView(generics.ListAPIView):
    queryset = store_models.Product.objects.all()
    serializer_class = restful_serializer.ProductSerializer
    search_fields = ['title', 'brand__title', 'category__title', ]
    ordering_fields = ('id', 'price',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter,
                       )
    filter_class = restful_filters.ProductFilter
    pagination_class = WithTotalPagesCountPagination


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = restful_serializer.ProductSerializer
    lookup_url_kwarg = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug')
        if str(slug).isnumeric():
            kwargs = {'pk': self.kwargs.get('slug')}
        else:
            kwargs = {'slug': self.kwargs.get('slug')}
        instance = store_models.Product.objects.filter(**kwargs)
        if instance.exists():
            return instance.first()
        else:
            raise Http404()


class ProductReviewsView(generics.ListAPIView):
    serializer_class = restful_serializer.ReviewSerializer

    def get_queryset(self):
        return store_models.Review.objects.filter(product_id=self.kwargs.get('pk'))


class SlidersView(generics.ListAPIView):
    queryset = app_models.Slider.objects.all()
    serializer_class = restful_serializer.SliderSerializer


class UserView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = restful_serializer.UserSerializer

    def get_object(self):
        return self.request.user


class OrdersView(generics.ListCreateAPIView):
    permission_classes = [restful_permissions.DenyListAllowCreate, ]
    serializer_class = restful_serializer.OrderSerializer

    def get_queryset(self):
        return store_models.Order.objects.filter(customer=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = restful_serializer.OrderSerializer
    queryset = store_models.Order.objects.all()


class ProductAvailableListView(views.APIView):

    def post(self, request, *args, **kwargs):
        print(request.data)
        return response.Response(request.data)


class UserRegisterView(views.APIView):

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        username = data.get('username')
        if username and data.get('password'):
            if User.objects.filter(username=username).exists():
                return response.Response('Бундай фойдаланувчи мавжуд', status=status.HTTP_409_CONFLICT)
            else:
                user = User()
                user.username = data.get('username')
                user.set_password(data.get('password'))
                user.save()
                if data.get('phone'):
                    app_models.Profile(phone_number=data.get('phone'), user=user).save()
                return response.Response('Мувоффаққиятли рўйхатдан ўтилди', status=status.HTTP_201_CREATED)

        return response.Response('Хатолик')
