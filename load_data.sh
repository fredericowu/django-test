#!/bin/sh
. python3/bin/activate

python project/manage.py importardb --bill-of-materials input_data/bill_of_materials.csv  --price-quote input_data/price_quote.csv --comp-boss input_data/comp_boss.csv  --limpar-base

