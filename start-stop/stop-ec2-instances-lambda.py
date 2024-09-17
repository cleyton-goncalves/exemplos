# Função Lambda: stop-ec2-instances-lambda
# 
# Descrição:
# Esta função é responsável por desligar instâncias EC2 com base em tags específicas. 
# Ela filtra as instâncias que possuem as tags 'Env' e 'AUTOSTOP', ambas com os valores 
# definidos como 'DEV' e 'TRUE', respectivamente. Assim como a função de inicialização, 
# as comparações de tags são sensíveis a maiúsculas e minúsculas (case sensitive), o que 
# exige uma correspondência exata. As instâncias que atenderem aos critérios serão 
# desligadas.
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
    
    # Filtrar instâncias com as tags 'Env: DEV' e 'AUTOSTOP: TRUE'
    filters = [
        {'Name': 'tag:ENV', 'Values': ['DEV']},
        {'Name': 'tag:AUTOSTOP', 'Values': ['TRUE']}
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

    # Coleta IDs das instâncias que estão rodando
    instance_ids = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
        if instance['State']['Name'] == 'running'  # Verifica apenas instâncias rodando
    ]
    
    # Se houver instâncias rodando, executa o stop
    if instance_ids:
        try:
            ec2_client.stop_instances(InstanceIds=instance_ids)
            logger.info(f'Instâncias {instance_ids} foram desligadas')
        except Exception as e:
            logger.error(f"Erro ao parar instâncias: {str(e)}")
            return {
                'statusCode': 500,
                'body': f"Erro ao parar instâncias: {str(e)}"
            }
    else:
        logger.info('Nenhuma instância para desligar')

    return {
        'statusCode': 200,
        'body': f'Instâncias desligadas: {instance_ids}' if instance_ids else 'Nenhuma instância para desligar'
    }
