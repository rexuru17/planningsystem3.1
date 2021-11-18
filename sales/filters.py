import django_filters
from sales.models import PlanItem, SalesPlan, SalesRecords


class SalesRecordsFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', label='Sales Records from:')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', label='Sales Records to:')

    class Meta:
        model = SalesRecords
        fields = '__all__'
        exclude = ('quantity', 'date', 'customer')


class PlanItemFilter(django_filters.FilterSet):

    class Meta:
        model = PlanItem
        fields = '__all__'


class SalesPlanFilter(django_filters.FilterSet):
    

    class Meta:
        model = SalesPlan
        fields = '__all__'
        