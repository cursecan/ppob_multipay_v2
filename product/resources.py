from import_export import resources
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget


from .models import (
    Product, Group, Operator
)


class GroupResource(resources.ModelResource):
    class Meta:
        model = Group
        fields = [
            'code', 'group_name'
        ]
        export_order = [
            'code', 'group_name'
        ]
        import_id_fields = ['code']
        skip_unchanged = True
        report_skipped = False


class OperatorResource(resources.ModelResource):
    # group = resources.Field(
    #     attribute='group', column_name='group', 
    #     widget=ManyToManyWidget(Group, field='code')
    # )

    class Meta:
        model = Operator
        fields = [
            'code', 'operator_name'
        ]
        export_order = [
            'code', 'operator_name'
        ]
        import_id_fields = ['code']
        skip_unchanged = True
        report_skipped = False


class ProductResource(resources.ModelResource):
    group = resources.Field(
        attribute='group', column_name='group',
        widget=ForeignKeyWidget(Group, 'code')
    )
    operator = resources.Field(
        attribute='operator', column_name='operator',
        widget=ForeignKeyWidget(Operator, 'code')
    )

    class Meta:
        model = Product
        fields = [
            'code', 'product_name',
            'type_product',
            'operator', 'group',
            'nominal', 'price', 'commision',
        ]
        export_order = [
            'code', 'product_name',
            'type_product',
            'operator', 'group',
            'nominal', 'price', 'commision',
        ]
        import_id_fields = ['code']
        skip_unchanged = True
        report_skipped = False
       