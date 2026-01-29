import pytest
import pandas as pd
import os
from unittest.mock import MagicMock, patch
from src.connectors.loader import SupabaseLoader

@patch.dict(os.environ, {"SUPABASE_URL": "http://test-url.com", "SUPABASE_KEY": "test-key"})
class TestSupabaseLoader:
    
    def test_loader_initializes_successfully_with_env_vars(self):
        """Test successful initialization with env vars."""
        loader = SupabaseLoader()
        assert loader.supabase is not None

    @patch("src.connectors.loader.load_dotenv")
    def test_loader_raises_error_when_env_vars_are_missing(self, mock_load_dotenv):
        """Test initialization failure when env vars are missing."""
        with patch.dict(os.environ, clear=True):
            with pytest.raises(ValueError, match="must be set in the environment"):
                SupabaseLoader()

    @patch("src.connectors.loader.create_client")
    def test_fetch_data_handles_pagination_correctly(self, mock_create_client):
        """Test data fetching with simulated pagination."""
        # Setup mock client
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client
        
        # Instantiate loader (will use mock_create_client)
        loader = SupabaseLoader()
        loader.supabase = mock_client
        
        # Mock the chain: table(name).select("*").range(start, end).execute()
        # We need to simulate 2 calls: one returning data, next returning empty to stop loop
        
        # Batch 1: 1000 rows (full batch)
        batch_1 = [{"id": i, "val": i*2} for i in range(1000)]
        # Batch 2: 500 rows (partial batch, should stop after this)
        batch_2 = [{"id": i, "val": i*2} for i in range(1000, 1500)]
        
        # Mock responses
        response_1 = MagicMock()
        response_1.data = batch_1
        
        response_2 = MagicMock()
        response_2.data = batch_2
        
        # Configure the execute method to return response_1 then response_2
        # Note: In the actual code, it calls execute() on the result of range()
        # structure: client.table().select().range().execute()
        
        mock_table = mock_client.table.return_value
        mock_select = mock_table.select.return_value
        mock_range = mock_select.range.return_value
        mock_range.execute.side_effect = [response_1, response_2]

        # Call method
        df = loader.fetch_data("test_table", limit=5000)
        
        # Assertions
        assert len(df) == 1500
        assert list(df.columns) == ["id", "val"]
        assert mock_client.table.call_count == 2
        
    @patch("src.connectors.loader.create_client")
    def test_fetch_data_returns_empty_dataframe_for_empty_table(self, mock_create_client):
        """Test fetching from an empty table."""
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client
        
        loader = SupabaseLoader()
        loader.supabase = mock_client
        
        # Return empty data immediately
        response_empty = MagicMock()
        response_empty.data = []
        
        mock_client.table.return_value.select.return_value.range.return_value.execute.return_value = response_empty

        df = loader.fetch_data("empty_table")
        
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_save_raw_stores_data_correctly_as_csv(self, tmp_path):
        """Test saving dataframe to CSV."""
        loader = SupabaseLoader() # Mocked env vars from class decorator
        
        df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        output_path = tmp_path / "data" / "raw" / "test.csv"
        
        loader.save_raw(df, str(output_path))
        
        assert output_path.exists()
        loaded_df = pd.read_csv(output_path)
        pd.testing.assert_frame_equal(df, loaded_df)
