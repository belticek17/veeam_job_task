import os
import shutil
import time
import hashlib
import argparse
import logging


def calculate_md5(file_path):
    """Calculate the MD5 checksum of a file, which basically checks if the files are identical."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def sync_folders(source, replica, log_file):
    """Synchronize the contents of the replica folder with the source folder."""
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    # Ensure the source and replica paths are absolute paths
    source = os.path.abspath(source)
    replica = os.path.abspath(replica)
    log_file = os.path.abspath(log_file)  # Ensure log file is an absolute path

    # Traverse the source folder
    for directory_path, directory_names, file_names in os.walk(source):
        relative_path = os.path.relpath(directory_path, source)
        replica_directory_path = os.path.join(replica, relative_path)

        # Create directories in the replica if they don't exist
        if not os.path.exists(replica_directory_path):
            os.makedirs(replica_directory_path)
            logging.info(f"Directory created: {replica_directory_path}")
            print(f"Directory created: {replica_directory_path}")

        # Synchronize files
        for file in file_names:
            source_file = os.path.join(directory_path, file)
            replica_file = os.path.join(replica_directory_path, file)

            # Skip the log file to prevent it from being deleted or copied
            if os.path.abspath(replica_file) == log_file:
                continue

            # Copy the file if it doesn't exist in replica or if the contents differ
            if not os.path.exists(replica_file) or calculate_md5(source_file) != calculate_md5(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f"File copied: {source_file} to {replica_file}")
                print(f"File copied: {source_file} to {replica_file}")

    # Remove files and directories from replica that are not in source
    for directory_path, directory_names, file_names in os.walk(replica, topdown=False):
        relative_path = os.path.relpath(directory_path, replica)
        source_dirpath = os.path.join(source, relative_path)

        for file in file_names:
            replica_file = os.path.join(directory_path, file)
            source_file = os.path.join(source_dirpath, file)

            # Skip the log file
            if os.path.abspath(replica_file) == log_file:
                continue

            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info(f"File removed: {replica_file}")
                print(f"File removed: {replica_file}")

        # Remove empty directories in the replica that don't exist in the source
        if not os.path.exists(source_dirpath) and os.path.isdir(directory_path):
            os.rmdir(directory_path)
            logging.info(f"Directory removed: {directory_path}")
            print(f"Directory removed: {directory_path}")


def main():
    parser = argparse.ArgumentParser(description='Synchronize 2 folders: source and its replica.')
    parser.add_argument('source', type=str, help='Source folder path')
    parser.add_argument('replica', type=str, help='Replica folder path')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', type=str, help='Log file path')

    args = parser.parse_args()

    source = args.source
    replica = args.replica
    interval = args.interval
    log_file = args.log_file

    while True:
        sync_folders(source, replica, log_file)
        time.sleep(interval)


if __name__ == "__main__":
    main()
