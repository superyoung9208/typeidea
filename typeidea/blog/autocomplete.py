from dal import autocomplete
from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    """文章类型自动补全"""

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Category.objects.none()
        qs = Category.objects.filter(owner=self.request.user).order_by('-id')
        if self.q:
            qs = qs.filter(name__startswith=self.q)
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    """标签自动补全"""

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()
        qs = Tag.objects.filter(owner=self.request.user).order_by('-id')
        if self.q:
            qs = qs.filter(name__startswith=self.request.q)
        return qs
