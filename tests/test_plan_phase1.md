# Plan de Pruebas - Fase 1: Carga de Datos

Este documento define la estrategia de pruebas para la Fase 1 del proyecto "Forecast Pyme Empanadas", centrada en la conexión y descarga de datos desde Supabase.

## Objetivos de la Prueba
1.  Verificar la correcta conexión con Supabase utilizando las credenciales del entorno.
2.  Validar la lógica de paginación y descarga en la clase `SupabaseLoader`.
3.  Asegurar que los datos descargados (`ventas_raw`) cumplan con la estructura y volumen esperados.
4.  Garantizar el manejo de errores ante fallos de red o credenciales inválidas.

## Alcance
-   **Componente:** `src/connectors/loader.py`
-   **Notebook:** `notebooks/01_data_loading.ipynb`
-   **Datos:** Tabla `ventas_raw` en Supabase.

## Estrategia de Pruebas

### 1. Pruebas Unitarias (Unit Tests)
Estas pruebas se ejecutarán aisladas de la base de datos real, utilizando `mocks` para simular la respuesta de Supabase.

*   **Archivo:** `tests/test_loader.py`
*   **Casos de Prueba:**
    *   **`test_init_missing_env_vars`**: Verificar que `SupabaseLoader` lance `ValueError` si faltan `SUPABASE_URL` o `SUPABASE_KEY`.
    *   **`test_fetch_data_pagination`**: Mocker la respuesta de `supabase.table().select().execute()` para simular paginación (ej. devolver 2 lotes de datos y luego vacío) y verificar que `fetch_data` concatene correctamente.
    *   **`test_fetch_data_empty`**: Simular una tabla vacía y verificar que devuelva un DataFrame vacío con las columnas esperadas (si se define esquema) o simplemente vacío.
    *   **`test_save_raw`**: Verificar que el método guarde el archivo en la ruta especificada y cree los directorios si no existen.

### 2. Pruebas de Integración
Estas pruebas conectan con el proyecto real de Supabase (requiere `.env` configurado).

*   **Archivo:** `tests/test_integration_supabase.py`
*   **Casos de Prueba:**
    *   **`test_connection_live`**: Instanciar `SupabaseLoader` y realizar una consulta simple (`limit=1`) para validar credenciales y conectividad.
    *   **`test_fetch_raw_schema`**: Descargar una muestra de `ventas_raw` y validar que existan las columnas críticas: `fecha`, `id_punto_venta`, `producto`, `cantidad`, etc.

### 3. Validación de Datos (Notebook/Script)
Validaciones a ejecutar sobre el archivo descargado (`data/01_raw/ventas.csv`).

*   **Script/Notebook:** `notebooks/01_data_loading.ipynb`
*   **Criterios de Aceptación:**
    *   **Volumen:** El archivo no debe estar vacío.
    *   **Formato:** Validar separador (CSV estándar) y codificación (UTF-8).
    *   **Tipos de Datos:** La columna de fecha debe ser convertible a datetime sin errores masivos.

## Ejecución de Pruebas

### Prerrequisitos
-   Entorno virtual activo.
-   Variables de entorno `SUPABASE_URL` y `SUPABASE_KEY` configuradas.
-   Paquetes instalados: `pytest`, `pandas`, `supabase`.

### Comandos
```bash
# Ejecutar todas las pruebas
pytest tests/

# Ejecutar solo unitarias
pytest tests/test_loader.py

# Ejecutar solo integración
pytest tests/test_integration_supabase.py
```
