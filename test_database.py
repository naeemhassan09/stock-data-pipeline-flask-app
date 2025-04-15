# This script tests the database connection and functionality of storing a DataFrame to a database table.
# This approach streamlined the process, ensured comprehensive coverage
# used AI to generate the test cases, and allowed more time to focus on integrating and refining the overall system.
import unittest
import os
import pandas as pd
from sqlalchemy.engine import Engine
from database import get_engine, table_exists, store_df_to_db

class TestDatabaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Optionally, set environment variables for testing.
        # Replace these values with valid credentials for your test database.
        os.environ["DB_USER"] = "testuser"
        os.environ["DB_PASSWORD"] = "testpassword"
        os.environ["DB_HOST"] = "localhost"
        os.environ["DB_PORT"] = "5432"
        os.environ["DB_NAME"] = "test_database"  # Ensure that this database exists.

    def test_get_engine(self):
        # Test that get_engine returns a non-None engine of type Engine.
        engine = get_engine()
        self.assertIsNotNone(engine)
        self.assertIsInstance(engine, Engine)
        engine.dispose()

    def test_store_and_table_exists(self):
        # Create a sample DataFrame for testing.
        df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6]
        })
        table_name = "test_table"
        
        # If the table already exists, drop it first.
        if table_exists(table_name):
            engine = get_engine()
            with engine.connect() as conn:
                conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            engine.dispose()
        
        # Store the DataFrame in the table.
        store_df_to_db(df, table_name)
        
        # Verify that the table now exists.
        self.assertTrue(table_exists(table_name))
        
        # Optionally, read the table and check that data was stored correctly.
        engine = get_engine()
        df_read = pd.read_sql_table(table_name, engine)
        engine.dispose()
        self.assertListEqual(list(df_read.columns), list(df.columns))  # Check column names.
        self.assertEqual(len(df_read), len(df))  # Check that the number of rows match.
        
        # Clean up by dropping the test table.
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        engine.dispose()

if __name__ == '__main__':
    unittest.main()