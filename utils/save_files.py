import os
import tempfile
import json
from datetime import datetime
import shutil
from pathlib import Path

def save_json(
    path,
    data
):
    directory = os.path.dirname(path) or "."

    with tempfile.NamedTemporaryFile(
        mode = 'w',
        encoding = 'utf-8',
        dir = directory,
        delete = False
    ) as file:
        json.dump(
            data,
            file, 
            indent = 4
        )
        temp_path = file.name

    os.replace(temp_path, path)

def create_backup_folder(dst_dir):
    dst_dir = Path(dst_dir)

    if not dst_dir.is_dir():
        raise FileNotFoundError(f"Directory {dst_dir} not found")

    timestamp = datetime.now().strftime("%d_%b_%Y_%H%M%S")
    backup_path = dst_dir / timestamp

    backup_path.mkdir(parents=True, exist_ok=False)

    return backup_path

def backup_data(
    src_dir,
    src_file_name,
    dst_dir,
    dst_file_name = None,
):

    src_path = Path(src_dir) / src_file_name
    dst_dir = Path(dst_dir)

    if not src_path.is_file():
        raise FileNotFoundError(f"Source file {src_path} not found")

    if not dst_dir.is_dir():
        raise FileNotFoundError(f"Destination directory {dst_dir} not found")

    if dst_file_name is None:
        dst_file_name = src_file_name

    dst_path = dst_dir / dst_file_name

    shutil.copy2(src_path, dst_path)

    print(f"Backup successful: {dst_path}")