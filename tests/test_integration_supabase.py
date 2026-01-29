import pytest
import os
import pandas as pd
from dotenv import load_dotenv
from src.connectors.loader import SupabaseLoader

# Load env vars
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@pytest.mark.skipif(not SUPABASE_URL or not SUPABASE_KEY, reason="Supabase credentials not found in env")
class TestSupabaseIntegration:
    
    def test_verify_supabase_authentication_and_connectivity(self):
        """Test real connection to Supabase."""
        loader = SupabaseLoader()
        # Fetch just 1 row to verify auth and existence
        try:
            df = loader.fetch_data("ventas_raw", limit=1)
            assert isinstance(df, pd.DataFrame)
            # We don't assert not empty because table might be empty initially
        except Exception as e:
            pytest.fail(f"Connection to Supabase failed: {e}")

    def test_validate_expected_columns_in_ventas_raw_table(self):
        """Test that the remote table has expected columns."""
        loader = SupabaseLoader()
        df = loader.fetch_data("ventas_raw", limit=5)
        
        if df.empty:
            pytest.skip("ventas_raw table is empty, cannot verify schema")
            
        expected_columns = [
            "fecha", "region", "punto_venta", "tipo", 
            "unidades_vendidas", "precio_venta", "ingresos_totales"
        ]
        # Check if expected columns are a subset of actual columns
        actual_cols = [c.lower() for c in df.columns]
        
        for col in expected_columns:
            assert col in actual_cols, f"Column {col} missing from Supabase table"
