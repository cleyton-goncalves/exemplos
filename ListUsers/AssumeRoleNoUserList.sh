#!/bin/bash

# Perfil e região AWS CLI
PROFILE="inbursa_payer"
REGION="us-east-1"

# Função para verificar o último login de um usuário
check_last_login() {
  local user=$1
  # Obter eventos de login do CloudTrail relevantes
  logins=$(aws cloudtrail lookup-events --profile $PROFILE --region $REGION --lookup-attributes AttributeKey=Username,AttributeValue=$user --query "Events[?EventName=='AssumeRole'].EventTime" --output table)

  if [ -z "$logins" ]; then
    echo "Usuário $user não tem eventos de login."
  else
    echo "Último login do usuário $user: $(echo "$logins" | sort | tail -n 1)"
  fi
}

# Obter todos os eventos de AssumeRole do CloudTrail
events=$(aws cloudtrail lookup-events --profile $PROFILE --region $REGION --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRole --query "Events[].{User:Username,Event:EventName,Time:EventTime}" --output json)

# Extrair usuários únicos dos eventos
users=$(echo "$events" | jq -r '.[].User' | sort | uniq)

# Iterar sobre a lista de usuários e verificar o último login de cada um
for user in $users; do
  check_last_login "$user"
done
