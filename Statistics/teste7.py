import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Dados da imagem
data = {
    "Serviço": ["Total de Serviço", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"],
    "EC2-Outros($)": [733.18, 116.69, 94.90, 114.17, 114.65, 115.92, 176.84],
    "VPC($)": [575.44, 20.14, 18.67, 125.57, 212.50, 85.54, 113.01],
    "Key Management Service($)": [493.06, 82.10, 82.19, 82.06, 82.17, 82.16, 82.38],
    "Tax($)": [284.03, 4.73, 4.54, 61.20, 78.20, 58.20, 77.16],
    "Security Hub($)": [236.92, 39.30, 36.46, 40.59, 40.79, 39.14, 40.65],
    "Kinesis($)": [183.14, 31.17, 29.15, 31.17, 30.21, 31.22, 30.23],
    "EC2-Instâncias($)": [113.43, 7.44, 0.67, 12.54, 45.99, 13.25, 33.53],
    "CloudWatch($)": [90.45, 5.74, 5.01, 6.00, 8.07, 24.36, 41.25],
    "GuardDuty($)": [83.51, 12.88, 11.69, 13.28, 13.09, 15.10, 17.47],
    "Inspector($)": [50.03, 15.94, 14.39, 4.09, 4.00, 3.88, 7.73],
    "S3($)": [30.06, 4.42, 4.42, 4.70, 4.80, 5.27, 6.45],
    "Config($)": [29.67, 4.43, 3.19, 6.59, 6.88, 2.61, 5.96]
}

# Criar DataFrame
df = pd.DataFrame(data)

# Definir 'Serviço' como o índice
df.set_index('Serviço', inplace=True)

# Análise estatística
stats = df.describe()
print("Análise Estatística:\n", stats)

# Gráfico de Barras: Total de Serviço
plt.figure(figsize=(16, 10))
df.loc['Total de Serviço'].plot(kind='bar', color='skyblue')
plt.title('Total de Serviço Breakdown')
plt.ylabel('Cost ($)')
plt.xlabel('Service')
plt.show()

# Gráfico de Linhas: Custos Mensais por Serviço
df.drop('Total de Serviço').plot(kind='line', figsize=(16, 10), marker='o')
plt.title('Monthly Service Costs')
plt.ylabel('Cost ($)')
plt.xlabel('Month')
plt.legend(loc='upper left')
plt.show()

# Gráfico de Pizza: Distribuição do Total de Serviço
plt.figure(figsize=(12, 12))
df.loc['Total de Serviço'].plot(kind='pie', autopct='%1.1f%%')
plt.title('Total de Serviço Distribution')
plt.ylabel('')
plt.show()

# Previsão dos próximos 3 meses
df_forecast = df.drop("Total de Serviço")

# DataFrame para armazenar as previsões
forecast_df = pd.DataFrame(index=["Julho", "Agosto", "Setembro"], columns=df.columns)

# Aplicar Holt-Winters Exponential Smoothing para cada coluna e prever os próximos 3 meses
for column in df_forecast.columns:
    model = ExponentialSmoothing(df_forecast[column], trend='add', seasonal=None, seasonal_periods=None)
    fit = model.fit()
    forecast = fit.forecast(3)
    forecast_df[column] = forecast.values

# Combinar o DataFrame original com a previsão
df_combined = pd.concat([df, forecast_df])

# Plotando a previsão
plt.figure(figsize=(16, 10))
for column in df.columns:
    plt.plot(df_combined.index, df_combined[column], marker='o', label=column)

plt.title('Previsão dos Custos Mensais por Serviço para Julho, Agosto e Setembro')
plt.ylabel('Custo ($)')
plt.xlabel('Mês')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.grid(True)
plt.show()

print("Previsões para Julho, Agosto e Setembro:\n", forecast_df)
