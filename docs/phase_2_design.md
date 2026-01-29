# Diseño Técnico - Fase 2: Transformación Estricta (Daily -> Monthly)

## 1. Objetivo
Convertir los datos transaccionales diarios en series de tiempo mensuales agregadas de forma pura. En esta fase **NO se realiza imputación** de valores faltantes; el objetivo es obtener la "fuente de verdad" agregada para que el equipo de expertos decida la estrategia de relleno en la **Fase 3: Data Preparation**.

## 2. Insumos
- **Fuente**: `data/01_raw/ventas_raw.csv`.
- **Periodo de interés**: 2018-01-01 hasta 2025-12-31.

## 3. Workflow de Transformación (Strict Mode)

### Paso 1: Limpieza de Calidad (Nivel Diario)
1.  **Tratamiento de Valores Centinela**:
    - Unidades `-1`, `999`, `9999` convertidas a `NaN`.
2.  **Normalización de Categorías**:
    - Estandarización a Mayúsculas y eliminación de espacios en `Ciudad`, `Producto`, `Canal`.
    - Mapeo de nulos a `'OTROS'`.

### Paso 2: Agregación Mensual Pura
1.  Truncar fechas al mes (`YYYY-MM-01`).
2.  Agrupar por `mes_fecha`, `ciudad`, `producto`, `canal`.
3.  Sumarizar `unidades`. Si no hay ventas reportadas para una combinación en un mes, el registro simplemente no existirá en este punto (No-Imputation).

### Paso 3: Aplicación de la Regla de Oro (Cutoff)
- Filtrar estrictamente hasta el **31 de diciembre de 2025**.

## 4. Entregables Técnicos
1.  **Archivo Maestro**: `data/02_cleansed/ventas_mensuales.parquet`.
2.  **Reporte de Integridad (`outputs/reports/p2_transformation_report.md`)**:
    - Validación de que la suma mensual coincide con la diaria.
3.  **Metadatos (`outputs/reports/p2_transformation_stats.json`)**.

## 5. Criterios de Aceptación
- La suma de unidades post-agregación coincide con la suma pre-agregación.
- Todas las categorías están normalizadas.
- **Nota**: Se permiten huecos temporales (gaps) para análisis posterior.
