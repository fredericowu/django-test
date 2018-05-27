#!/bin/bash
md5=$(which md5 || which md5sum)

input_price_quote="input_data/price_quote.csv"
output_price_quote="exports/out_price_quote.csv"

input_comp_boss="input_data/comp_boss.csv"
output_comp_boss="exports/out_comp_boss.csv"

input_bill="input_data/bill_of_materials.csv"
output_bill="exports/out_bill_of_materials.csv"


. python3/bin/activate
python project/manage.py exportarcsv

function check_files {
  input=$1
  output=$2

  md5_input=$(sort $input | $md5 | awk '{ print $1 }')
  md5_output=$(sort $output | $md5 | awk '{ print $1 }')

  if [ "$md5_input" = "$md5_output" ]; then
    echo $(basename $input) " OK" 
    else
      echo $(basename $input) " NOK - Erro na verifição :("
      echo $md5_input
      echo $md5_output
  fi
}
echo "Testando se arquivos exportados são identicos a arquivos importados"

check_files $input_price_quote $output_price_quote
check_files $input_comp_boss $output_comp_boss
check_files $input_bill $output_bill



