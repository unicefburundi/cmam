import django_tables2 as tables


class SortieTable(tables.Table):
    entee = tables.Column(verbose_name="Entrees")
    sortie = tables.Column(verbose_name="Sorties")
    restant = tables.Column(verbose_name="Stock Restant")

    class Meta:
        attrs = {"class": "table ", "data-toggle": "table", "data-search": "true","data-show-columns": "true",  "data-show-export": "true", 'data-export-types': "['csv','excel']"}

    def render_restant(self, record):

        return record.entee - record.sortie
