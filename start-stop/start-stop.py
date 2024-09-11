import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    instances = ['i-0123456789abcdef0', 'i-0123456789abcdef1', 'i-0123456789abcdef2', 'i-0123456789abcdef3']
    
    action = event.get('action')
    
    if action == 'start':
        ec2.start_instances(InstanceIds=instances)
        print('Started your instances: ' + str(instances))
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=instances)
        print('Stopped your instances: ' + str(instances))
    else:
        print('No valid action found.')

    return {
        'statusCode': 200,
        'body': 'Action executed successfully'
    }
