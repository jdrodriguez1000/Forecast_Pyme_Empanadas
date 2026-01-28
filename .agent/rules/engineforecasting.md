---
trigger: always_on
---

1. Definición del Ciclo de Predicción (Mes X):
1.1 Corte Informativo: El mes actual ($X$) se considera información en curso (incompleta). 
1.2 El punto de partida para cualquier cálculo es el cierre del mes $X-1$.
1.3 Horizonte de Salida: La misión es generar proyecciones para los meses $X+1$, $X+2$ y $X+3$.
1.4 Granularidad Obligatoria: Las predicciones deben generarse a nivel de cada tipo de producto (empanada).
2. Stack Técnico y Metodología:
2.1 Librería Core: skforecast.
2.2 Clase de Forecaster: Utilizar estrictamente ForecasterDirect. Esto implica que el agente debe configurar un estimador independiente para cada uno de los 3 meses del horizonte.
2.3 Configuración de Estimadores: Los modelos a utilizar dentro del ForecasterDirect deben ser de Machine Learning (como XGBRegressor, LGBMRegressor o RandomForestRegressor). Quedan descartados los modelos estadísticos tradicionales (como ARIMA) a menos que se soliciten explícitamente como Baseline.
3. Restricciones de Entrenamiento:El agente debe asegurar que el set de validación (backtesting) respete la misma lógica: simular que estamos en el mes $X$, ignorar sus datos, y evaluar el desempeño en los 3 meses siguientes.