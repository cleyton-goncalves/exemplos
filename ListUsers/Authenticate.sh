#!/bin/bash

# Perfil e região AWS CLI
PROFILE="inbursa_payer"
REGION="us-east-1"

# Lista de usuários
USERS=(
"abel.junior@matera.com"
"adeilson.araujo@claro.com.br"
"alan.albuquerque@matera.com"
"albert.thome@matera.com"
"alexandre.gomessantos@claro.com.br"
"anderson.canciano@matera.com"
"anderson.lima@matera.com"
"andre.jesus@matera.com"
"arnaldo.filho@matera.com"
"artur.junior@matera.com"
"aws-1085570@operacaomulticloud.com"
"aws-1085570-1@operacaomulticloud.com"
"aws-1085570-2@operacaomulticloud.com"
"aws-inbursa-backup@operacaomulticloud.com"
"aws-inbursa-deployment@operacaomulticloud.com"
"aws-inbursa-jumpbox@operacaomulticloud.com"
"aws-inbursa-network@operacaomulticloud.com"
"aws-inbursa-perimeter@operacaomulticloud.com"
"aws-inbursa-prod@operacaomulticloud.com"
"aws-inbursa-uat@operacaomulticloud.com"
"charlles.sousa@matera.com"
"claudio.vieira@matera.com"
"cristiano.martins@matera.com"
"daniel.bessa@claro.com.br"
"deiverson.takano@claro.com.br"
"delphino.araujo@matera.com"
"emanuel.mazzer@matera.com"
"enrico.taboga@matera.com"
"everton.silva@matera.com"
"fabricio.doscruz@claro.com.br"
"fernando.francis@matera.com"
"flavio.bastos@matera.com"
"gilson.junior@matera.com"
"guilherme.mendonca@matera.com"
"guilherme.vilela@matera.com"
"hamilton.paes@matera.com"
"igor.camillo@matera.com"
"jheimmys.toggweiler@matera.com"
"joao.silva@matera.com"
"jodemi.santos@globalhitss.com.br"
"jorge.carvalho@matera.com"
"jose.ramos@inbursa.com"
"josiel.oliveira@matera.com"
"kelvin.tatarevic@claro.com.br"
"krodriguezc@inbursa.com"
"lfsanchezc@inbursa.com"
"lucas.cunha@matera.com"
"lucas.dantas@matera.com"
"luiz.calegari@matera.com"
"luiz.saraiva@matera.com"
"marcio.jardim@matera.com"
"marco.pontes@matera.com"
"marcus.alcantara@matera.com"
"matias.schweizer@matera.com"
"mauricio.vasconcelos@inbursa.com"
"mcuamatzig@inbursa.com"
"miespinosac@inbursa.com"
"msanchezz@inbursa.com"
"murilo.prado@matera.com"
"nicolas.guimaraes@inbursa.com"
"nilson.castro@matera.com"
"nilva.gaspar@matera.com"
"paulo.santos@matera.com"
"raphael.brangioni@matera.com"
"raphael.toledo@matera.com"
"ricardo.carvalho@matera.com"
"rodrigo.santos@inbursa.com"
"sinesio.neto@matera.com"
"victor.espindola@matera.com"
"vinicius.valerio@matera.com"
"willer.santos@matera.com"
"william.halter@matera.com"
"william.sparremberger@matera.com"
)

# Função para verificar o último login de um usuário
check_last_login() {
  local user=$1
  # Obter eventos de login do CloudTrail
  logins=$(aws cloudtrail lookup-events --profile $PROFILE --region $REGION --lookup-attributes AttributeKey=Username,AttributeValue=$user --query "Events[?EventName=='Authenticate'].EventTime" --output table)

  if [ -z "$logins" ]; then
    echo "Usuário $user não tem eventos de login."
  else
    echo "Último login do usuário $user: $(echo "$logins" | sort | tail -n 1)"
  fi
}

# Iterar sobre a lista de usuários e verificar o último login de cada um
for user in "${USERS[@]}"; do
  check_last_login "$user"
done
