import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os
import requests

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    
    # Use requests to download the file (fix for Windows)
    with open(csv_name, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)

    # Create SQLAlchemy engine
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()

    # Use the downloaded CSV file
    df = pd.read_csv(csv_name)

    if 'lpep_pickup_datetime' in df.columns:
        df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])

    if 'lpep_dropoff_datetime' in df.columns:
        df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    
    # Print schema of the dataframe
    print(pd.io.sql.get_schema(df, name=table_name, con=engine))

    # Reading the file in chunks
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=10000)

    while True:
        try:
            t_start = time()
            
            df = next(df_iter)
            
            if 'lpep_pickup_datetime' in df.columns:
                df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime']) 
            if 'lpep_dropoff_datetime' in df.columns:
                df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
                
            # Inserting the chunk into the database
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            
            t_end = time()
            
            print(f'Inserted another chunk, took {t_end - t_start:.3f} seconds')

        except StopIteration:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', help='username for Postgres')
    parser.add_argument('--password', help='password for Postgres')  
    parser.add_argument('--host', help='host for Postgres')
    parser.add_argument('--port', help='port for Postgres')
    parser.add_argument('--db', help='database for Postgres')
    parser.add_argument('--table_name', help='table for Postgres')
    parser.add_argument('--url', help='URL of the CSV file')

    params = parser.parse_args()
    main(params)
   