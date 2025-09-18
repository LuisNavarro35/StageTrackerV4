import mysql.connector
from mysql.connector import Error
import config

# =========================
# CONNECTION FUNCTION
# =========================
def get_connection(db_name):
    """
    Returns a connection object to the specified database.
    """
    try:
        connection = mysql.connector.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=db_name
        )
        if connection.is_connected():
            print(f"✅ Successfully connected to database: {db_name}")
            return connection
    except Error as e:
        print(f"❌ Error connecting to database {db_name}: {e}")
        return None

# =========================
# EXAMPLES / TEST FUNCTION
# =========================
def test_connections():
    # Connect to AssetManager DB (users)
    am_conn = get_connection(config.DB_NAME_ASSETMANAGER)
    if am_conn:
        cursor = am_conn.cursor()
        cursor.execute("SELECT username, is_admin FROM user LIMIT 5;")
        rows = cursor.fetchall()
        print("Sample Users from AssetManagerDB:")
        for row in rows:
            print(row)
        am_conn.close()

    # Connect to StageTracker DB (jobs, counters)
    st_conn = get_connection(config.DB_NAME)
    if st_conn:
        cursor = st_conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Tables in StageTrackerDB:")
        for t in tables:
            print(t)
        st_conn.close()


# =========================
# ENTRY POINT FOR TESTING
# =========================
if __name__ == "__main__":
    test_connections()
