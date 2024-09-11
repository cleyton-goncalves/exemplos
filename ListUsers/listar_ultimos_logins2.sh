#!/bin/bash

# Perfil e região AWS CLI
PROFILE="inbursa_payer"
REGION="us-east-1"

# Função para obter o último login de um usuário
get_last_login() {
  USERNAME=$1
  aws cloudtrail lookup-events \
    --region $REGION \
    --lookup-attributes AttributeKey=EventName,AttributeValue=ConsoleLogin AttributeKey=Username,AttributeValue=$USERNAME \
    --query 'Events[?Resources[?ResourceName==`'"$USERNAME"'`]].EventTime | [0]' \
    --output text \
    --profile $PROFILE
}

# Lista de usuários manualmente definida
USERS=(
  "marcio.jardim@matera.com"
  "fernando.francis@matera.com"
  "anderson.lima@matera.com"
  "everton.silva@matera.com"
  "william.halter@matera.com"
  "kelvin.tatarevic@claro.com.br"
  "willer.santos@matera.com"
  "jose.ramos@inbursa.com"
  "enrico.taboga@matera.com"
  "mauricio.vasconcelos@matera.com"
  "joao.silva@matera.com"
  "marcus.alcantara@matera.com"
  "lucas.dantas@matera.com"
  "jorge.carvalho@matera.com"
)

# Cabeçalho da tabela
printf "%-30s %-30s\n" "Usuário" "Último Login"
printf "%-30s %-30s\n" "------" "------------"

# Loop através dos usuários e obtenha o último login
for USER in "${USERS[@]}"; do
  LAST_LOGIN=$(get_last_login $USER)
  printf "%-30s %-30s\n" "$USER" "$LAST_LOGIN"
done
