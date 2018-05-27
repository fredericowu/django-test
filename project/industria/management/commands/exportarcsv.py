from django.core.management.base import BaseCommand, CommandError
from industria.importador import Importador
import argparse

class Command(BaseCommand):
    help = 'Exporta as bases em CSV (formato original): bill_of_materials.csv, price_quote.csv, comp_boss.csv'

    def handle(self, *args, **options):
        bill_of_materials = open("exports/out_bill_of_materials.csv", 'wt')
        price_quote       = open("exports/out_price_quote.csv", 'wt')
        comp_boss         = open("exports/out_comp_boss.csv", 'wt')

        exportacao = Importador( bill_of_materials, price_quote, comp_boss )

        self.stdout.write( "Exportando arquivos CSV" )
        importacao_ok = exportacao.exportar()
        if importacao_ok:
            self.stdout.write(self.style.SUCCESS('Arquivos exportados com sucesso'))

