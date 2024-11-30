import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy import stats

# Преобразование с использованием Box-Cox
def boxcox_df(x):
    x_boxcox, _ = stats.boxcox(x)
    return x_boxcox

# Пример данных (замените на ваши данные)
rfm_data = pd.DataFrame({
    'amount': [100, 200, 300, 5000, 10000, 2500],  # Пример сумм транзакций
    'frequency': [5, 3, 8, 10, 15, 4],  # Пример частоты транзакций
    'relationship_duration': [365, 200, 1500, 100, 120, 365],  # Пример длительности отношений
    'last_payment_days': [30, 60, 365, 1, 5, 2]  # Пример дней с последней оплаты
})

# Преобразуем данные с помощью Box-Cox
rfm_data_boxcox = rfm_data.apply(boxcox_df, axis=0)

# Нормализуем данные
scaler = StandardScaler()
rfm_norm = scaler.fit_transform(rfm_data_boxcox)

# Вычисление оптимального числа кластеров с помощью Elbow метода
sse = {}
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(rfm_norm)
    sse[k] = kmeans.inertia_

# Оптимальное количество кластеров (например, 3)
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(rfm_norm)

# Расстояние до центроида для каждой точки
distances = kmeans.transform(rfm_norm)

# Выявление аномалий по 97-му процентилю
threshold = np.percentile(distances, 97)
predictions = (distances >= threshold).astype(int)

# Добавление результатов в исходные данные
rfm_data['Cluster'] = kmeans.labels_
rfm_data['Anomaly'] = predictions

# График Heatmap (средние значения признаков для каждого кластера)
cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=rfm_data.columns[:-2])  # без колонок 'Cluster' и 'Anomaly'
sns.heatmap(cluster_centers, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title('Heatmap of Cluster Centers')
plt.show()

# График Snake plot (различия между кластерами)
cluster_means = rfm_data.groupby('Cluster').mean()
cluster_means.plot(kind='line', marker='o', figsize=(8, 6))
plt.title('Snake Plot: Differences Between Clusters')
plt.xlabel('Cluster')
plt.ylabel('Mean Value of Features')
plt.grid(True)
plt.show()

# Сохранение результатов в файл preds.csv
rfm_data['Anomaly'] = rfm_data['Anomaly'].map({0: False, 1: True})  # Преобразуем 0/1 в True/False
rfm_data['Anomaly'].to_csv('preds.csv', index=False, header=False)

# Вывод информации о результатах
print(rfm_data[['amount', 'frequency', 'relationship_duration', 'last_payment_days', 'Cluster', 'Anomaly']])
