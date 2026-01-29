# Fase 1: Reporte de Carga de Datos (Data Ingestion)

## 1. Principales Hallazgos
- **Volumen de Datos**: Se cargaron exitosamente **30099 registros** provenientes de la tabla `ventas_raw` de Supabase.
- **Estructura**: El dataset cuenta con **11 columnas**, incluyendo dimensiones geográficas, temporales y financieras.
- **Rango Temporal**: Los datos cubren desde el **2018-01-01** hasta el **2025-12-31**.
- **Integridad Inicial**: No se detectaron valores nulos técnicos en la carga inicial.

## 2. Principales Inconvenientes
- **Valores Centinela**: Se requiere limpieza de valores 0 o negativos en unidades/precios en la Fase 2.
- **Paginación**: La carga masiva requiere gestión de offsets para evitar timeouts de la API.

## 3. Sugerencias
- **Optimización de Formato**: Considerar Parquet para mejorar el rendimiento de lectura.
- **Monitoreo de Drift**: Implementar alertas si la carga diaria cae significativamente.

## 4. Recomendaciones
- **Fase de Transformación**: Iniciar la limpieza siguiendo las reglas de negocio de valores centinela numéricos y categóricos.
- **Resguardo de Crudos**: No modificar `ventas_raw.csv` directamente.

## 5. Conclusiones
La ingestión de datos ha sido exitosa. El dataset es íntegro y el volumen es suficiente para iniciar el análisis y modelado.
