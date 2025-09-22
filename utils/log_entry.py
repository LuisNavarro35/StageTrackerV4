import json
import config
from db.connection import get_connection

def add_log_entry_db(job_id, user_name, event_type, new_value, message):
    try:
        conn = get_connection(db_name=config.DB_NAME)
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO logs (job_id, user_name, event_type, new_value, message)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    job_id,
                    user_name,
                    event_type,
                    json.dumps(new_value) if new_value is not None else None,
                    message
                )
            )
            conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging to DB: {e}")

