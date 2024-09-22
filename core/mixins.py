from django.db.models import Q

class SearchMixin:
    print("Search mixin")
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        print("Query", query)
        if query:
            search_queries = Q()
            # Combine the search fields from the mixin and the view
            combined_search_fields = self.search_fields + getattr(self, 'extra_search_fields', [])
            print("Combined search fields: ", combined_search_fields)
            for field in combined_search_fields:
                search_queries |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(search_queries)

        return queryset
