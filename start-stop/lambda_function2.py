import boto3

# Obtendo a região da sessão atual
region = boto3.session.Session().region_name
ec2_client = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    # Obtendo ação e IDs das instâncias do evento
    action = event.get('action')
    instance_ids = event.get('instanceIds')
    exclude_ids = event.get('excludeIds', [])

    # Filtrar instâncias que não estão na lista de exclusão
    instance_ids = [i for i in instance_ids if i not in exclude_ids]
    
    # Validando se ação e IDs das instâncias estão presentes no evento
    if not action or not instance_ids:
        raise ValueError("Evento deve conter 'action' e 'instanceIds'")
    
    if action == 'start':
        ec2_client.start_instances(InstanceIds=instance_ids)
        print(f'Instâncias {instance_ids} foram iniciadas.')
    elif action == 'stop':
        ec2_client.stop_instances(InstanceIds=instance_ids)
        print(f'Instâncias {instance_ids} foram desligadas.')
    else:
        raise ValueError(f"Ação desconhecida: {action}")
