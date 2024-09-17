# Função Lambda: start-ec2-instances-lambda
# 
# Descrição:
# Esta função é responsável por iniciar instâncias EC2 com base em tags específicas. 
# Ela filtra as instâncias que possuem as tags 'Env' e 'AUTOSTART', ambas com os valores 
# definidos como 'DEV' e 'TRUE', respectivamente. Para evitar problemas de sensibilidade 
# de maiúsculas e minúsculas (case sensitive), a função utiliza o método upper() nas 
# comparações das tags. Caso existam instâncias com essas tags, elas são iniciadas 
# automaticamente.
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
    
    # Filtros de instâncias com tags 'Env' e 'AUTOSTART'
    filters = [
        {'Name': 'tag:Env', 'Values': ['DEV']},
        {'Name': 'tag:AUTOSTART', 'Values': ['TRUE']}
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

    # Coleta IDs das instâncias que precisam ser ligadas
    instance_ids = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
        if all(tag['Key'].upper() == 'ENV' and tag['Value'].upper() == 'DEV' for tag in instance.get('Tags', [])) and
           all(tag['Key'].upper() == 'AUTOSTART' and tag['Value'].upper() == 'TRUE' for tag in instance.get('Tags', []))
    ]
    
    # Se houver instâncias a iniciar, inicia as instâncias
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
