import pandas as pd
import matplotlib.pyplot as plt

# Dados fornecidos
colunas = [
    "Serviço", "EC2-Outros($)", "VPC($)", "Key Management Service($)", "Tax($)", 
    "Security Hub($)", "Kinesis($)", "EC2-Instâncias($)", "CloudWatch($)", 
    "GuardDuty($)", "Inspector($)", "S3($)", "Config($)"
]

dados = [
    ["Total de Serviço", 733.18, 575.44, 493.06, 284.03, 236.92, 183.14, 113.43, 90.45, 83.51, 50.03, 30.06, 29.67],
    ["Janeiro", 116.69, 20.14, 82.10, 4.73, 39.30, 31.17, 7.44, 5.74, 12.88, 15.94, 4.42, 4.43],
    ["Fevereiro", 94.90, 18.67, 82.19, 4.54, 36.46, 29.15, 0.67, 5.01, 11.69, 14.39, 4.42, 3.19],
    ["Março", 114.17, 125.57, 82.06, 61.20, 40.59, 31.17, 12.54, 6.00, 13.28, 4.09, 4.70, 6.59],
    ["Abril", 114.65, 212.50, 82.17, 78.20, 40.79, 30.21, 45.99, 8.07, 13.09, 4.00, 4.80, 6.88],
    ["Maio", 115.92, 85.54, 82.16, 58.20, 39.14, 31.22, 13.25, 24.36, 15.10, 3.88, 5.27, 2.61],
    ["Junho", 176.84, 113.01, 82.38, 77.16, 40.65, 30.23, 33.53, 41.25, 17.47, 7.73, 6.45, 5.96]
]

# Criação do DataFrame
df = pd.DataFrame(dados, columns=colunas)

# Gráfico de barras - Custos totais por mês
plt.figure(figsize=(12, 6))
df.set_index('Serviço').loc[['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho']].plot(kind='bar', stacked=True)
plt.title('Custos Totais por Serviço (Janeiro a Junho)')
plt.ylabel('Custos ($)')
plt.xlabel('Mês')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
