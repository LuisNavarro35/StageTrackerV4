# db/connection.py
import pymysql
import traceback
import config

def get_connection(db_name):
    """
    Returns a PyMySQL connection to the specified database, or None on failure.
    Signature preserved as get_connection(db_name) so other code does not change.
    """
    try:
        connection = pymysql.connect(
            host=config.DB_HOST,
            port=int(config.DB_PORT),
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=db_name,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10
        )
        # Successful connection — return the connection object
        print(f"✅ Successfully connected to database: {db_name}")
        return connection

    except Exception as e:
        # Print the exception + stack trace for debugging (safe in dev)
        print(f"❌ Error connecting to database {db_name}: {e}")
        traceback.print_exc()
        return None
