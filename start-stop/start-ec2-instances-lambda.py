# Função Lambda: start-ec2-instances-lambda
# 
# Descrição:
# Esta função é responsável por iniciar instâncias EC2 com base em tags específicas. 
# Ela filtra as instâncias que possuem as tags 'Env' e 'AUTOSTART', ambas com os valores 
# definidos como 'DEV' e 'TRUE', respectivamente. A função realiza comparações de tags 
# de forma exata, portanto, é sensível a maiúsculas e minúsculas (case sensitive). 
# Caso existam instâncias com essas tags, elas são iniciadas automaticamente.
# 
# Entradas:
# - Nenhuma entrada é exigida explicitamente (evento é opcional).
# 
# Saídas:
# - Status de sucesso (200) e lista de instâncias iniciadas, ou mensagem informando 
#   que não há instâncias para iniciar.

import boto3
import logging


# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Filtrar instâncias com as tags 'Env: DEV' e 'AUTOSTART: TRUE'
    filters = [
        {'Name': 'tag:ENV', 'Values': ['DEV']},
        {'Name': 'tag:AUTOSTART', 'Values': ['TRUE']}
    ]
    
    try:
        # Recupera as instâncias com base nos filtros
        response = ec2_client.describe_instances(Filters=filters)
    except Exception as e:
        logger.error(f"Erro ao descrever instâncias: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Erro ao descrever instâncias: {str(e)}"
        }

    # Coleta IDs das instâncias que estão no estado 'stopped' (paradas)
    instance_ids = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
        if instance['State']['Name'] == 'stopped'  # Verifica apenas instâncias que estão paradas
    ]
    
    # Se houver instâncias paradas, executa o start
    if instance_ids:
        try:
            ec2_client.start_instances(InstanceIds=instance_ids)
            logger.info(f'Instâncias {instance_ids} foram iniciadas')
        except Exception as e:
            logger.error(f"Erro ao iniciar instâncias: {str(e)}")
            return {
                'statusCode': 500,
                'body': f"Erro ao iniciar instâncias: {str(e)}"
            }
    else:
        logger.info('Nenhuma instância para iniciar')

    return {
        'statusCode': 200,
        'body': f'Instâncias iniciadas: {instance_ids}' if instance_ids else 'Nenhuma instância para iniciar'
    }
