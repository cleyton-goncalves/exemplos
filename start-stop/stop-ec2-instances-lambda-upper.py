import boto3
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Filtros de instâncias com tags 'Env' e 'AUTOSTART' (sem upper() aqui, pois o filtro é direto)
    filters = [
        {'Name': 'tag:Env', 'Values': ['DEV']},
        {'Name': 'tag:AUTOSTART', 'Values': ['TRUE']}
    ]
    
    try:
        # Descreve instâncias com os filtros
        response = ec2_client.describe_instances(Filters=filters)
        logger.info(f"Resposta da AWS EC2: {response}")  # Adicionando log para ver a resposta da API
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
        if any(tag['Key'].upper() == 'ENV' and tag['Value'].upper() == 'DEV' for tag in instance.get('Tags', [])) and
           any(tag['Key'].upper() == 'AUTOSTART' and tag['Value'].upper() == 'TRUE' for tag in instance.get('Tags', []))
    ]
    
    # Registrar IDs das instâncias encontradas antes de desligar
    logger.info(f"Instâncias encontradas para desligar: {instance_ids}")
    
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
