import os
from sqlalchemy import create_engine, inspect

def get_engine():
    # Get PostgreSQL connection details from environment variables
    user = os.getenv("DB_USER", "your_username")
    password = os.getenv("DB_PASSWORD", "your_password")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "financial_data")
    
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(connection_string)
    return engine

def table_exists(table_name):
    engine = get_engine()
    inspector = inspect(engine)
    exists = table_name in inspector.get_table_names()
    engine.dispose()
    return exists

def store_df_to_db(df, table_name):
    engine = get_engine()
    try:
        df.to_sql(table_name, engine, if_exists="replace", index=True)
        print(f"Data stored in table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error storing data in table '{table_name}': {e}")
    finally:
        engine.dispose()