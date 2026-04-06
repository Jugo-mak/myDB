import psycopg2
from psycopg2 import sql

conn_params = {
    "dbname": "tents",
    "user": "postgres",
    "password": "agtj8512",
    "host": "localhost",
    "port": "5433"
}

try:
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    
    # テーブル一覧を取得
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    
    print("--- Tables in tents database ---")
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        
        # 各テーブルのカラム情報を取得
        cur.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """)
        columns = cur.fetchall()
        for col in columns:
            print(f"  - {col[0]}: {col[1]} (Nullable: {col[2]})")

    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
