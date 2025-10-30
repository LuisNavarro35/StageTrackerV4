import json
import config
import os
from datetime import datetime
from db.connection import get_connection

def add_log_entry_db(job_id, job_name, user_name, event_type, new_value, message):
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

        # 2️⃣ Log locally to a per-job file
        save_job_log(job_name, job_id, user_name, event_type, new_value, message)


    except Exception as e:
        print(f"Error logging to DB: {e}")
        # Still log locally even if DB fails
        save_job_log(job_name, job_id, user_name, event_type, new_value, f"DB ERROR: {e}")


def save_job_log(job_name, job_id, user_name, event_type, new_value, message):
    """Append log entry to a per-job text file; creates file with header if missing."""
    try:
        # Ensure ./logs directory exists
        documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
        log_dir = os.path.join(documents_dir, "StageTrackerAppData", "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Clean job name for filename safety
        safe_job_name = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in job_name)
        log_file_path = os.path.join(log_dir, f"{safe_job_name}.txt")

        # Check if file exists
        file_exists = os.path.isfile(log_file_path)

        # Open file in append mode
        with open(log_file_path, "a", encoding="utf-8") as f:
            # Write header if file was just created
            if not file_exists:
                creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                header = (
                    f"{'='*70}\n"
                    f" Stage Tracker Job Log File\n"
                    f" Job Name : {job_name}\n"
                    f" Created  : {creation_time}\n"
                    f"{'='*70}\n"
                    f" Format:\n"
                    f" [Timestamp] JOB_ID | USER | EVENT | NEW_VALUE | MESSAGE\n"
                    f"{'-'*70}\n"
                )
                f.write(header)

            # Write actual log entry
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if new_value is not None:
                formatted_value = f"\n{json.dumps(new_value, ensure_ascii=False, indent=2)}"
            else:
                formatted_value = " None"

            entry = (
                f"[{timestamp}] JOB_ID={job_id} | USER={user_name} | EVENT={event_type} |\n"
                f"NEW_VALUE={formatted_value}\nMESSAGE={message}\n{'-' * 70}\n"
            )
            f.write(entry)

    except Exception as e:
        print(f"Error saving local log for job '{job_name}': {e}")