import os


def ensure_dir_exists(folder_path: str):
    if folder_path and not os.path.exists(folder_path):
        os.makedirs(folder_path)
