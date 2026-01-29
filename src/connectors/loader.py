import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

class SupabaseLoader:
    """
    Handles data loading from Supabase.
    """
    def __init__(self):
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the environment or .env file.")
            
        self.supabase: Client = create_client(url, key)

    def fetch_data(self, table_name: str, limit: int = 100000) -> pd.DataFrame:
        """
        Fetches data from a specified Supabase table.
        Args:
            table_name: The name of the table to fetch from.
            limit: The maximum number of rows to fetch.
        Returns:
            pd.DataFrame: The fetched data.
        """
        print(f"Fetching data from table: {table_name}...")
        
        all_data = []
        offset = 0
        batch_size = 1000
        
        while True:
            response = self.supabase.table(table_name).select("*").range(offset, offset + batch_size - 1).execute()
            data = response.data
            
            if not data:
                break
                
            all_data.extend(data)
            offset += batch_size
            print(f"Fetched {len(all_data)} rows...")
            
            if len(data) < batch_size or len(all_data) >= limit:
                break
                
        df = pd.DataFrame(all_data)
        print(f"Total rows fetched: {len(df)}")
        return df

    def save_raw(self, df: pd.DataFrame, filepath: str):
        """
        Saves the DataFrame to a CSV file.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
