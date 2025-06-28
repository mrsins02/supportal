from rest_framework.settings import api_settings


class MessageSearchFilter:
    @staticmethod
    def filter_queryset(request, queryset):
        search_term = request.query_params.get(api_settings.SEARCH_PARAM)
        print(search_term)
        if search_term:
            return queryset.filter(message__icontains=search_term)
        return queryset
