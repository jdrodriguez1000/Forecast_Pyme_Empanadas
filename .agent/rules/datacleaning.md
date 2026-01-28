---
trigger: always_on
---

1. Validación de Completitud:
1.1 Serie Temporal: El agente debe verificar que no existan saltos en las fechas por cada combinación de Ciudad-Producto-Canal. Si faltan meses, debe aplicar imputación por interpolación lineal o Forward Fill, justificando la elección en un Artifact.
1.2 Datos Nulos: Identificar NaN o nulos. No eliminarlos de entrada; evaluar si corresponden a un punto de venta nuevo (inicio de serie) o una falta de reporte.

2. Detección de Valores Centinelas por Tipo: El agente debe limpiar los datos basándose en estos patrones antes de cualquier análisis:
2.1 Numéricos (unidades): Identificar 0 (donde debería haber venta), -1, 999, o 9999. Tratarlos como nulos y proceder a su imputación.
2.2 Categorías (Ciudad/Producto/Pago): Identificar 'NULL', 'N/A', 'UNDEFINED' o espacios vacíos. Mapearlos a la categoría correcta o marcarlos como 'OTROS'.
2.3 Booleanos: Normalizar valores inconsistentes (ej. convertir 'S', '1', 'True' a un formato booleano real).
2.4 Fechas: Validar que no existan fechas "época" (ej. 1900-01-01 o 1970-01-01) que sesguen la serie temporal.
3. Tratamiento de Valores Atípicos (Outliers):
El agente debe proponer un umbral (ej. 3 desviaciones estándar o método IQR) para detectar picos de venta inusuales que no correspondan a las temporadas de fin/mitad de año definidas en el contexto de negocio.