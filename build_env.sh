#!/bin/bash
# testado em Mac e Ubuntu


pip=$(which pip || which pip3)
python3=$(which python3 || which python)
virtualenv=$(which virtualenv)

if [ "$python3" != "" ]; then
  python_version=$($python3 -V 2>&1 | awk '{ print $2 }' | awk -F\. '{ print $1 }')
fi

if [ "$python3" = "" ] || [ "$python_version" != "3" ]; then
  echo "Precisa ter python3 :("
  echo $python3
  echo $python_version
  exit 1
fi



# Instalando o virtualenv
if [ "$virtualenv" = "" ]; then
  echo "Instalando virtualenv com o pip, forneca senha root"
  sudo $pip install virtualenv
fi


# Criando um ambiente virtual com python3
echo "Criando ambiente virtual python"
virtualenv --python=$python3 python3

# Entrando no ambiente virtual e instalando requerimentos
echo "Instalando requerimentos"
. python3/bin/activate
pip install -r requirements.txt 
python project/manage.py migrate

mkdir -p exports

echo "####################################################"
echo "Forneça os dados que serão utilizados para acessar a interface de administracao"
python project/manage.py createsuperuser


