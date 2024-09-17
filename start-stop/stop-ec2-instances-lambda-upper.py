# Função Lambda: stop-ec2-instances-lambda
# 
# Descrição:
# Esta função é responsável por desligar instâncias EC2 com base em tags específicas. 
# Ela filtra as instâncias que possuem as tags 'Env' e 'AUTOSTOP', ambas com os valores 
# definidos como 'DEV' e 'TRUE', respectivamente. Assim como a função de inicialização, 
# o método upper() é utilizado nas comparações de tags para evitar problemas relacionados 
# à sensibilidade de maiúsculas e minúsculas (case sensitive). As instâncias que atenderem 
# aos critérios serão desligadas.
# 
# Entradas:
# - Nenhuma entrada é exigida explicitamente (evento é opcional).
# 
# Saídas:
# - Status de sucesso (200) e lista de instâncias desligadas, ou mensagem informando 
#   que não há instâncias para desligar.

import boto3
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Filtros de instâncias com tags 'Env' e 'AUTOSTOP'
    filters = [
        {'Name': 'tag:Env', 'Values': ['DEV']},
        {'Name': 'tag:AUTOSTOP', 'Values': ['TRUE']}
    ]
    
    try:
        # Descreve instâncias com os filtros
        response = ec2_client.describe_instances(Filters=filters)
    except Exception as e:
        logger.error(f"Erro ao descrever instâncias: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Erro ao descrever instâncias: {str(e)}"
        }

    # Coleta IDs das instâncias que precisam ser desligadas
    instance_ids = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
        if all(tag['Key'].upper() == 'ENV' and tag['Value'].upper() == 'DEV' for tag in instance.get('Tags', [])) and
           all(tag['Key'].upper() == 'AUTOSTOP' and tag['Value'].upper() == 'TRUE' for tag in instance.get('Tags', []))
    ]
    
    # Se houver instâncias a desligar, desliga as instâncias
    if instance_ids:
        try:
            ec2_client.stop_instances(InstanceIds=instance_ids)
            logger.info(f'Instâncias {instance_ids} foram desligadas')
        except Exception as e:
            logger.error(f"Erro ao desligar instâncias: {str(e)}")
            return {
                'statusCode': 500,
                'body': f"Erro ao desligar instâncias: {str(e)}"
            }
    else:
        logger.info('Nenhuma instância para desligar')

    return {
        'statusCode': 200,
        'body': f'Instâncias desligadas: {instance_ids}' if instance_ids else 'Nenhuma instância para desligar'
    }
