import os
import tempfile
import json
from datetime import date
import shutil
import sys

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

def create_backup_folder(
    dst_dir,
    date_of_backup
):
    if not os.path.exists(dst_dir):
        raise FileNotFoundError(f"Directory {dst_dir} not found")

    if isinstance(date_of_backup, date):
        date_format = date_of_backup.strftime("%d_%b_%Y")

        backup_folder_path = str(dst_dir) + date_format

        if os.path.exists(backup_folder_path):
            shutil.rmtree(backup_folder_path)

        os.makedirs(backup_folder_path)

        return backup_folder_path + "\\"
    
    else:
        raise ValueError(f"Provided date is invalid")

        

def backup_data(
    date_of_backup,
    src_dir = '',
    src_file_name = None,
    dst_dir = '',
    dst_file_name = None,
):

    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Directory {src_dir} not found")
    
    if src_file_name is None:
        raise ValueError("Please give a source file name")

    if not isinstance(date_of_backup, date):
        raise ValueError("Date is invalid")
    
    try:

        date_format = str(date_of_backup.strftime("%d_%b_%Y_"))

        if dst_file_name is None:
            dst_file_name = src_file_name

        src_dir = src_dir + src_file_name
        
        if not os.path.exists(src_dir):
            raise FileNotFoundError(f"Source file {src_dir} not found")
    
        if src_file_name and dst_file_name and src_dir and dst_dir:
            dst_dir = dst_dir + dst_file_name
        
        elif dst_file_name is None or not dst_file_name:
            dst_file_name = src_file_name
            dst_dir = dst_dir + dst_file_name
    
        elif dst_file_name.isspace():
            dst_file_name = src_file_name
            dst_dir = dst_dir + dst_file_name
    
        else:
            dst_dir = dst_dir + dst_file_name

        shutil.copy2(src_dir, dst_dir)
    
        print("Backup successful")

    except PermissionError:

        dst_dir = dst_dir + date_format + dst_file_name

        shutil.copytree(src_file_name, dst_dir)
    