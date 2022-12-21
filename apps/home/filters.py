import django_filters
from apps.home.models import Site, Interface, ApplicationPerInterface, InInterfaceBurst, OutInterfaceBurst
class ApplicationPerInterfaceFilter(django_filters.FilterSet):
    # app_name = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = ApplicationPerInterface
        fields = ['interface', ]
        """
        fields = {
            'app_name': ['exact', ],
            'interface': ['exact', ],
        }
        """


class InInterfaceBurstFilter(django_filters.FilterSet):
    class Meta:
        model = InInterfaceBurst
        fields = ['date', 'time', 'interface',]

class OutInterfaceBurstFilter(django_filters.FilterSet):
    class Meta:
        model = OutInterfaceBurst
        fields = ['date', 'time', 'interface',]