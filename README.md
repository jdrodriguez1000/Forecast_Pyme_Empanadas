# Forecast Pyme Empanadas

Este proyecto implementa un modelo de Machine Learning para optimizar la planeación de demanda de una Pyme de empanadas, con el objetivo de reducir el error de pronóstico actual (45%) y apoyar la toma de decisiones mediante un enfoque híbrido (Modelo + Ajuste de Expertos).

## 1. Contexto y Objetivos del Negocio

**Objetivo Principal:**
Reducir el error de planeación utilizando un modelo de ML como base (*Baseline*), sobre el cual el equipo de expertos aplicará sus conocimientos de mercado (*Expert Overlay*). El éxito se medirá comparando el error del modelo base contra el del ajuste experto final.

**Alcance del Pronóstico:**
*   **Horizonte:** 3 meses ($X+1$, $X+2$, $X+3$).
*   **Granularidad:**
    *   **Productos (SKUs):** Carne, Pollo, Queso, Mixta, Chicharrón, Arroz con Pollo, Hawaiana, Vegetariana, Jamón y Queso, Carne Desmechada.
    *   **Geografía:** Bogotá, Medellín, Cali, Barranquilla, Cartagena, Bucaramanga, Pereira, Manizales.
    *   **Canales:** Tienda, Calle, Centro Comercial, Delivery, Restaurante.
    *   **Métodos de Pago:** Efectivo, Tarjeta Débito, Tarjeta Crédito, Transferencia, Daviplata, Nequi.

## 2. Metodología de Pronóstico (Engine Forecasting)

El núcleo de pronóstico se basa en la librería **skforecast**.

*   **Estrategia:** `ForecasterDirect`. Se entrena un estimador independiente para cada paso del horizonte de predicción (meses 1, 2 y 3).
*   **Modelos:** Se utilizan algoritmos de Machine Learning puros como **XGBRegressor**, **LGBMRegressor** o **RandomForestRegressor**. (ARIMA y modelos estadísticos quedan excluidos salvo como baseline comparativo explícito).
*   **Ciclo de Predicción:**
    *   El mes actual ($X$) se considera información incompleta.
    *   Los datos de entrada llegan hasta el cierre del mes $X-1$.
    *   La validación (backtesting) simula este mismo escenario para garantizar métricas realistas.

## 3. Calidad y Limpieza de Datos

El pipeline asegura la integridad de los datos siguiendo reglas estrictas:

*   **Completitud:**
    *   Se validan saltos en la serie temporal para cada combinación Ciudad-Producto-Canal.
    *   Imputación de meses faltantes mediante interpolación lineal o *Forward Fill*.
*   **Manejo de Nulos:**
    *   No se eliminan registros nulos automáticamente; se evalúa si corresponden a nuevos puntos de venta o falta de reporte.
*   **Valores Centinela:**
    *   *Numéricos:* 0 (donde debería haber venta), -1, 999, 9999 se tratan como nulos para imputación.
    *   *Categóricos:* 'NULL', 'N/A', 'UNDEFINED' se mapean a categorías correctas o 'OTROS'.
    *   *Booleanos:* Normalización de 'S', '1', 'True' a booleano real.
    *   *Fechas:* Validación de fechas época (1900-01-01) para evitar sesgos.
*   **Outliers:** Se aplica detección de desviaciones (ej. > 3 std dev) para identificar picos de venta no estacionales.

## Estructura del Proyecto

*   `data/`: Almacena los sets de datos en sus diferentes estados (raw, cleansed, features).
*   `notebooks/`: Exploración y prototipado de modelos.
*   `src/`: Código fuente productivo (pipelines de limpieza, feature engineering, modelado).
*   `outputs/`: Métricas de desempeño y modelos serializados.

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
