from .forms import BRAND_SORT_CHOICES, FOOD_SORT_CHOICES


class FoodFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        brand = self.request.GET.get('brand')
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort')

        if q:
            queryset = queryset.filter(name__icontains=q)

        if brand:
            try:
                queryset = queryset.filter(brand=brand)
            except Exception:
                pass

        if category:
            try:
                queryset = queryset.filter(category=category)
            except Exception:
                pass

        if sort and any(sort in x for x in FOOD_SORT_CHOICES):
            queryset = queryset.order_by(sort)

        return queryset


class BrandFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        sort = self.request.GET.get('sort')

        if q:
            queryset = queryset.filter(name__icontains=q)

        if sort and any(sort in x for x in BRAND_SORT_CHOICES):
            queryset = queryset.order_by(sort)

        return queryset
