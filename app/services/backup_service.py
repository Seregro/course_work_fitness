import subprocess
import datetime
import os
from app.core.config import settings

def create_db_backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.sql"
    os.environ["PGPASSWORD"] = "password"
    cmd = [
        "pg_dump",
        "-h", "localhost",
        "-U", "postgres",
        "-d", "fitness_db",
        "-f", backup_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        return backup_file
    except Exception as e:
        print(f"Backup failed: {e}")
        return None

def upload_to_remote(file_path):
    remote_path = f"/tmp/remote_storage/{os.path.basename(file_path)}"
    os.makedirs(os.path.dirname(remote_path), exist_ok=True)
    import shutil
    shutil.move(file_path, remote_path)
    return remote_path