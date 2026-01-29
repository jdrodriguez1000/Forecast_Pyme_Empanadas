import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import List, Optional

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataTransformer:
    """
    Clase para manejar la transformación de datos de ventas diarias a mensuales,
    incluyendo limpieza de valores centinela, normalización e imputación.
    """
    
    def __init__(self, cutoff_date: str = "2025-12-31"):
        self.cutoff_date = pd.to_datetime(cutoff_date)
        self.sentinel_values = [-1, 999, 9999]
        
        # Mapeo de nombres de columnas reales
        self.col_map = {
            'region': 'ciudad',
            'tipo': 'producto',
            'punto_venta': 'canal',
            'unidades_vendidas': 'unidades',
            'metodo_pago': 'metodo_pago'
        }
        
        self.categorical_columns = ['ciudad', 'producto', 'canal', 'metodo_pago']
        self.dimensions = ['ciudad', 'producto', 'canal']

    def rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renombra las columnas del dataset original a nombres estándar."""
        return df.rename(columns=self.col_map)

    def clean_sentinels(self, df: pd.DataFrame) -> pd.DataFrame:
        """Reemplaza valores centinela por NaN."""
        df = df.copy()
        mask = df['unidades'].isin(self.sentinel_values)
        num_replaced = mask.sum()
        df.loc[mask, 'unidades'] = np.nan
        logger.info(f"Valores centinela detectados y reemplazados: {num_replaced}")
        return df

    def normalize_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza textos y maneja nulos en categorías."""
        df = df.copy()
        for col in self.categorical_columns:
            if col in df.columns:
                # Limpieza básica
                df[col] = df[col].astype(str).str.upper().str.strip()
                # Mapeo de nulos/indefinidos a 'OTROS'
                null_patterns = ['NULL', 'N/A', 'UNDEFINED', 'NAN', 'NONE', '']
                df.loc[df[col].isin(null_patterns), col] = 'OTROS'
        return df

    def filter_by_cutoff(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica la Regla de Oro: Filtrar hasta la fecha de corte."""
        df = df.copy()
        df['fecha'] = pd.to_datetime(df['fecha'])
        initial_rows = len(df)
        df = df[df['fecha'] <= self.cutoff_date]
        logger.info(f"Registros eliminados por fecha de corte (> {self.cutoff_date}): {initial_rows - len(df)}")
        return df

    def aggregate_monthly(self, df: pd.DataFrame) -> pd.DataFrame:
        """Agrupa las ventas diarias a nivel mensual por dimensiones."""
        df = df.copy()
        df['mes_fecha'] = df['fecha'].dt.to_period('M').dt.to_timestamp()
        
        monthly_df = df.groupby(['mes_fecha'] + self.dimensions)['unidades'].sum().reset_index()
        logger.info(f"Agregación mensual completada. Filas finales: {len(monthly_df)}")
        return monthly_df

    def fill_gaps(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Asegura que cada serie (Ciudad-Producto-Canal) sea continua.
        Rellena meses faltantes y aplica interpolación/ffill.
        """
        # Crear el grid completo de fechas
        min_date = df['mes_fecha'].min()
        max_date = self.cutoff_date.replace(day=1) # Asegurar que termina en el primer día del mes de corte
        all_months = pd.date_range(start=min_date, end=max_date, freq='MS')
        
        # Identificar combinaciones únicas
        combinations = df[self.dimensions].drop_duplicates()
        
        # Crear el index maestro
        multi_index = pd.MultiIndex.from_product(
            [all_months] + [combinations[c].unique() for c in self.dimensions],
            names=['mes_fecha'] + self.dimensions
        )
        
        # Reindexar
        master_df = pd.DataFrame(index=multi_index).reset_index()
        df_complete = pd.merge(master_df, df, on=['mes_fecha'] + self.dimensions, how='left')
        
        # Imputación por serie (Interpolación lineal + Ffill / Bfill para extremos)
        # Nota: En una implementación más robusta, usaríamos groupby y apply
        num_nans_before = df_complete['unidades'].isna().sum()
        
        df_complete['unidades'] = df_complete.groupby(self.dimensions)['unidades'].transform(
            lambda x: x.interpolate(method='linear').ffill().bfill()
        )
        
        num_nans_after = df_complete['unidades'].isna().sum()
        logger.info(f"Gaps rellenados. NaNs imputados: {num_nans_before - num_nans_after}")
        
        return df_complete

    def generate_report(self, df_original: pd.DataFrame, df_final: pd.DataFrame, output_dir: str = "outputs/reports"):
        """Genera reportes detallados enfocados en la integridad post-agregación."""
        import json
        import os
        from pathlib import Path

        os.makedirs(output_dir, exist_ok=True)
        
        df_renamed = self.rename_columns(df_original)
        
        # Validación de Integridad Estricta
        unidades_diarias_limpias = float(df_renamed['unidades'].replace(self.sentinel_values, np.nan).sum())
        unidades_mensuales_finales = float(df_final['unidades'].sum())
        
        diff = abs(unidades_diarias_limpias - unidades_mensuales_finales)
        integridad = diff < 0.01

        stats = {
            "fase": 2,
            "nombre": "Transformación Estándar (Sin Imputación)",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "integrity": {
                "total_input_clean": unidades_diarias_limpias,
                "total_output_monthly": unidades_mensuales_finales,
                "diff": diff,
                "check_ok": integridad
            },
            "dimensions": {
                "rows_raw": len(df_original),
                "rows_transformed": len(df_final)
            }
        }
        
        # Guardar JSON
        json_path = Path(output_dir) / "p2_transformation_stats.json"
        with open(json_path, 'w') as f:
            json.dump(stats, f, indent=4)
            
        # Reporte Markdown Simple y Honesto
        md_path = Path(output_dir) / "p2_transformation_report.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Fase 2: Reporte de Integridad de Transformación\n\n")
            f.write(f"## 1. Validación de Unidades\n")
            f.write(f"- **Unidades en Raw (después de limpiar ruidos):** {unidades_diarias_limpias:,.2f}\n")
            f.write(f"- **Unidades Mensuales Agregadas:** {unidades_mensuales_finales:,.2f}\n")
            f.write(f"- **Estatus:** {'✅ COINCIDENCIA TOTAL' if integridad else '❌ DISCREPANCIA DETECTADA'}\n\n")
            f.write(f"## 2. Decisión sobre el Proceso\n")
            f.write(f"Se ha eliminado la imputación automática por interpolación. El dataset actual **solo contiene ventas reales reportadas**. Los periodos sin ventas aparecen como registros ausentes en la serie.\n\n")
            f.write(f"## 3. Próximo Paso Crítico\n")
            f.write(f"En la Fase 3, debemos analizar si los huecos temporales representan cierres de puntos de venta o ventas en cero para decidir la estrategia de relleno manual.\n")
            
        logger.info(f"Reporte de integridad generado en: {md_path}")

    def run_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ejecuta transformación y agregación sin inventar datos."""
        logger.info("Iniciando pipeline de transformación Fase 2 (Modo Estricto)...")
        df_processed = (
            df.pipe(self.rename_columns)
              .pipe(self.filter_by_cutoff)
              .pipe(self.clean_sentinels)
              .pipe(self.normalize_categories)
              .pipe(self.aggregate_monthly)
              # .pipe(self.fill_gaps)  <-- SE ELIMINA LA IMPUTACIÓN AUTOMÁTICA
        )
        logger.info("Pipeline Fase 2 finalizado. Datos agregados pero sin completar gaps.")
        return df_processed
