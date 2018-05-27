from django.core.management.base import BaseCommand, CommandError
from industria.importador import Importador
import argparse

class Command(BaseCommand):
    help = 'Importa as bases em CSV: bill_of_materials.csv, price_quote.csv, comp_boss.csv'

    def add_arguments(self, parser):
        parser.add_argument('--bill-of-materials', required=True, type=argparse.FileType('r'), help='Caminho do bill_of_materials.csv')
        parser.add_argument('--price-quote', required=True, type=argparse.FileType('r'), help='Caminho do price_quote.csv')
        parser.add_argument('--comp-boss', required=True, type=argparse.FileType('r'), help='Caminho do comp_boss.csv')
        parser.add_argument('--limpar-base', action='store_true', help='Limpa a base antes de iniciar a importacao')


    def handle(self, *args, **options):
        bill_of_materials = options['bill_of_materials']
        price_quote       = options['price_quote']
        comp_boss         = options['comp_boss']

        importacao = Importador( bill_of_materials, price_quote, comp_boss )

        if options['limpar_base']:
            self.stdout.write( "Limpando base..." )
            importacao.limpar_base()

        self.stdout.write( "Importando arquivos CSV" )
        importacao_ok = importacao.importar()
        if importacao_ok:
            self.stdout.write(self.style.SUCCESS('Arquivos importados com sucesso'))

