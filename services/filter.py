from store.models import Watch
from django.contrib import messages
from django.db.models import Q

class WatchFilter:
    def filter(self, request):
        watches = Watch.total_price()

        filter_fields = {
            'min-price': 'total_price__gte',
            'max-price': 'total_price__lte',
            'categoryFilter': 'category__id',
            'dial_color': 'dial_color',
            'band_color': 'band_color',
            'styleFilter': 'style',
            'functionalityFilter': 'functionality',
            'materialFilter': 'material',
            'movementFilter': 'movement',
            'genderFilter': 'gender',
            'search': 'name__icontains',
        }

        filters = {}

        for name, field in filter_fields.items():
            # Check that the incoming filter name is in the dictionary
            if name in request.GET:
                get_name = request.GET.getlist(name)

                # Check if value is a list or a single value
                if len(get_name) == 1:
                    filters[field] = get_name[0]
                else:
                    # if filter value is list then use __in to get multiple objects
                    filters[f'{field}__in'] = get_name

        if filters:
            watches = watches.filter(**filters)


        if 'sort_by' in request.GET:
            sort_by = request.GET.get('sort_by')

            sort_query = {
                'newness': '-created_at',
                'popularity': '-view_count',
                'low': 'total_price',
                'high': '-total_price',
            }

            for sort in sort_query:
                if sort_by == sort:
                    # Get the field name to be sorted in the dictionary on the request
                    watches = watches.order_by(sort_query[sort])


        if 'load_more' in request.GET:
            get_load_more = int(request.GET.get('load_more'))

            if get_load_more < Watch.total_price().count():
                # 3 more objects are returned when there is a load request
                watches = watches[:get_load_more + 3]
            else:
                # Return error when there is no object to load
                messages.error(request, 'No more watch to load')

        else:
            watches = watches[:6]


        return {'watches': watches, 'filters': filters}
