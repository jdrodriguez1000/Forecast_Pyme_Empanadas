import pytest
import pandas as pd
import numpy as np
from src.preprocessing.transformer import DataTransformer

@pytest.fixture
def sample_data():
    """Genera datos de prueba para el transformer con nombres de columnas originales."""
    data = {
        'fecha': ['2025-01-01', '2025-01-15', '2025-02-01', '2026-01-01'],
        'region': ['Bogotá', 'bogota ', 'Medellín', 'Bogotá'],
        'tipo': ['CARNE', 'Carne', 'POLLO', 'CARNE'],
        'punto_venta': ['RESTAURANTE', 'Restaurante', 'DELIVERY', 'RESTAURANTE'],
        'unidades_vendidas': [10, 9999, 15, 20],
        'metodo_pago': ['EFECTIVO', 'EFECTIVO', 'TARJETA', 'EFECTIVO']
    }
    return pd.DataFrame(data)

def test_rename_columns(sample_data):
    transformer = DataTransformer()
    df_renamed = transformer.rename_columns(sample_data)
    assert 'ciudad' in df_renamed.columns
    assert 'producto' in df_renamed.columns
    assert 'canal' in df_renamed.columns
    assert 'unidades' in df_renamed.columns
    assert 'region' not in df_renamed.columns

def test_clean_sentinels(sample_data):
    transformer = DataTransformer()
    df = transformer.rename_columns(sample_data)
    df_clean = transformer.clean_sentinels(df)
    assert df_clean['unidades'].isna().sum() == 1
    assert np.isnan(df_clean.loc[1, 'unidades'])

def test_normalize_categories(sample_data):
    transformer = DataTransformer()
    df = transformer.rename_columns(sample_data)
    df_norm = transformer.normalize_categories(df)
    ciudades = df_norm['ciudad'].unique()
    assert all(c in ['BOGOTÁ', 'MEDELLÍN', 'BOGOTA', 'MEDELLIN'] for c in ciudades)
    productos = df_norm['producto'].unique()
    assert all(p in ['CARNE', 'POLLO'] for p in productos)

def test_filter_by_cutoff(sample_data):
    transformer = DataTransformer(cutoff_date="2025-12-31")
    df_filtered = transformer.filter_by_cutoff(sample_data)
    assert len(df_filtered) == 3
    assert all(df_filtered['fecha'] <= pd.Timestamp('2025-12-31'))

def test_aggregate_monthly(sample_data):
    transformer = DataTransformer()
    # Ejecutamos el pipeline parcial para probar agregación
    df = transformer.rename_columns(sample_data)
    df = transformer.normalize_categories(df)
    df['fecha'] = pd.to_datetime(df['fecha'])
    df_agg = transformer.aggregate_monthly(df)
    
    # Bogotá en Enero 2025 tiene 2 registros originales
    bogota_jan = df_agg[(df_agg['ciudad'].str.contains('BOGOTA')) & 
                        (df_agg['mes_fecha'] == '2025-01-01')]
    assert len(bogota_jan) >= 1
