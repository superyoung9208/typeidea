from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, viewsets

from blog.models import Post, Category
from blog.serializders import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer


# @api_view()
# def post_list(request):
#     posts = Post.objects.filter(status=Post.STATUS_NORMAL)
#     post_serializer = PostSerializer(posts, many=True)
#     return Response(post_serializer.data)
#
#
# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
#     serializer_class = PostSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """博客视图集"""
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        """博客详情"""
        self.serializer_class = PostDetailSerializer
        super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        """按类别过滤博客信息"""
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """文章类别试图集"""
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        """类别详情接口"""
        self.serializer_class = CategoryDetailSerializer  # 使用详情序列化器
        return super().retrieve(request, *args, **kwargs)
