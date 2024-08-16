# Folder Synchronizer

This repository contains a Python script that synchronizes two folders: `source` and `replica`. The script ensures that the `replica` folder is always an exact copy of the `source` folder. It performs periodic synchronization and logs all operations, including file creation, copying, and removal.

## Features

- **One-Way Synchronization**: Keeps the `replica` folder in sync with the `source` folder.
- **Periodic Execution**: Continuously monitors and updates the `replica` folder at a user-defined interval.
- **Logging**: Logs all file operations (creation, copying, removal) to both the console and a specified log file.
- **Error Handling**: Ensures correct handling of file paths and prevents unintended deletion of important files like the log file.

## Usage

1. **Run the Script**:
    ```sh
    python3 folder_synchronizer.py <source_folder_path> <replica_folder_path> <interval_in_seconds> <log_file_path>
    ```

   - `<source_folder_path>`: Path to the source folder that you want to replicate.
   - `<replica_folder_path>`: Path to the replica folder where the content will be synchronized.
   - `<interval_in_seconds>`: Time interval (in seconds) between each synchronization.
   - `<log_file_path>`: Path to the log file where synchronization activities will be logged.
