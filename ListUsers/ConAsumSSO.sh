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
"cleyton.goncalves@claro.com.br"
)

# Função para verificar o último login de um usuário
check_last_login() {
  local user=$1
  # Obter eventos de login do CloudTrail para ConsoleLogin e AssumeRole e possivelmente GetSSOStatus
  logins=$(aws cloudtrail lookup-events --profile $PROFILE --region $REGION --lookup-attributes AttributeKey=Username,AttributeValue=$user --query "Events[?EventName=='ConsoleLogin' || EventName=='AssumeRole' || EventName=='GetSSOStatus'].EventTime" --output table)

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
