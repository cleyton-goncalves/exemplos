import subprocess
import json

try:
    # Executar o comando AWS CLI
    users_result = subprocess.run(
        ["aws", "sso-admin", "list-users", "--instance-arn", "arn:aws:sso:::instance/ssoins-72231d6d69fb53ec", "--profile", "inbursa_payer"],
        capture_output=True,
        text=True,
        check=True
    )

    # Verificar se a saída não está vazia
    if users_result.stdout:
        print("Saída do comando AWS CLI:", users_result.stdout)
        # Carregar a saída como JSON
        users = json.loads(users_result.stdout)
        print(users)
    else:
        print("A saída do comando AWS CLI está vazia.")

except subprocess.CalledProcessError as e:
    print(f"O comando AWS CLI falhou com o código de erro {e.returncode}")
    print(e.output)

except json.JSONDecodeError as e:
    print("Falha ao decodificar a saída JSON")
    print(e.msg)
    print("Saída recebida:", users_result.stdout)

except Exception as e:
    print(f"Um erro inesperado ocorreu: {e}")
