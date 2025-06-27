import os


def ensure_dir_exists(folderPath: str):
    if folderPath and not os.path.exists(folderPath):
        os.makedirs(folderPath)
