#!/usr/bin/env python3
#~-~ encoding: utf-8 ~-~
#========================================================
# Created By:       Anthony Rodway
# Email:            anthony.rodway@nrcan-rncan.gc.ca
# Creation Date:    Fri November 10 14:00:00 PST 2023
# Organization:     Natural Resources of Canada
# Team:             Carbon Accounting Team
#========================================================
# File Header
#========================================================
"""
File: ripple_unzipple.py
Author: Anthony Rodway
Email: anthony.rodway@nrcan-rncan.gc.ca
Description: Recursively unzips all compressed folders in a given directory.

Usage:
    python ripple_unzipple.py input_path output_path [log_path]
"""


#========================================================
# Imports
#========================================================
import os
import sys
import time
import shutil
from datetime import datetime
from zipfile import ZipFile
from py7zr import SevenZipFile


#========================================================
# Global Classes
#========================================================
# ANSI escape codes for colors
class Colors:
    ERROR = '\033[91m'
    WARNING = '\033[93m'
    INFO = '\033[94m'
    END = '\033[0m'
      

#========================================================
# Error Handelling and Logging
#========================================================
def error_handeling(input_path, output_path):
    """ """
    # Check if the provided path exists
    if not os.path.exists(input_path):
        raise ValueError(f"The specified path does not exist: {input_path}")

    # Check if the provided path is a directory
    if not os.path.isdir(input_path):
        raise ValueError(f"The specified path is not a directory: {input_path}")

def log(path, type, message):
    """ """
    tag = 'ERROR'
    if type == Colors.INFO:
        tag = 'INFO'
    elif type == Colors.WARNING:
        tag = 'WARNING'
    print(f'{type}[{tag}] {message}{Colors.END}')
    
    if path != '':
        # Open the file in append mode
        with open(path, 'a') as log_file:
            # Append a log message
            log_file.write(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} [{tag}] {message}\n')
    

#========================================================
# Unzipping Functions
#========================================================
def ripple_unzip(input_path, output_path, log_path = ''):
    """ This function  """
    try:
        error_handeling(input_path, output_path)
        recursive_unzip(input_path, output_path)
    except Exception as error:
        log(log_path, Colors.ERROR, error)
        exit(1)
    
def recursive_unzip(input_path, output_path):
    """Recursively unzip .zip and .7z files in the input_path to the output_path."""
    # Create output_path if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Iterate through the directory and unzip any compressed folders
    for root, dirs, files in os.walk(input_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            new_file_path = ''
            if file.endswith(".zip"):
                with ZipFile(file_path, mode='r') as zip_ref:
                    file_path_no_extension = os.path.splitext(file_path)[0]
                    extract_path = os.path.join(output_path, file_path_no_extension[len(input_path) + 1:])
                    os.makedirs(extract_path, exist_ok=True)
                    zip_ref.extractall(extract_path)
                    recursive_unzip(extract_path, extract_path)  # Use extract_path as the new input_path
                    new_file_path = extract_path + '.zip'   
                    
                try:
                    os.remove(new_file_path)  # Remove the original compressed file from the new output folder
                except Exception as e:
                    print(f"Error removing file: {e}")            
                
            elif file.endswith(".7z"):
                with SevenZipFile(file_path, mode='r') as sevenzip_ref:
                    file_path_no_extension = os.path.splitext(file_path)[0]
                    extract_path = os.path.join(output_path, file_path_no_extension[len(input_path) + 1:])
                    os.makedirs(extract_path, exist_ok=True)
                    sevenzip_ref.extractall(extract_path)
                    recursive_unzip(extract_path, extract_path)  # Use extract_path as the new input_path
                    new_file_path = extract_path + '.7z'

                try:
                    os.remove(new_file_path)  # Remove the original compressed file from the new output folder
                except Exception as e:
                    print(f"Error removing file: {e}")

                
            
#========================================================
# Main
#========================================================
def main():
    """ The main function of the ripple_unzipple.py script """
    # Get the start time of the script
    start_time = time.time()
    print(f'\n{Colors.INFO}Tool is starting...{Colors.END}')
    
    try:
        # Get the path from the command-line argument
        if len(sys.argv) not in [3, 4]:
            raise ValueError("Usage: python ripple_unzipple.py input_path output_path [log_path]")

        # Call the recursive_unzip function with the provided path
        if len(sys.argv) == 4:
            ripple_unzip(sys.argv[1], sys.argv[2], sys.argv[3])

        ripple_unzip(sys.argv[1], sys.argv[2])
    except Exception as error:
        # print(f'{Colors.ERROR}[Error] {error}{Colors.END}')
        log(Colors.ERROR, error)
        exit(1)
        
    # Get the end time of the script and calculate the elapsed time
    end_time = time.time()
    print(f'\n{Colors.INFO}Tool has completed{Colors.END}')
    print(f'{Colors.INFO}Elapsed time: {end_time - start_time:.2f} seconds{Colors.END}')


#========================================================
# Main Guard
#========================================================
if __name__ == "__main__":
    sys.exit(main())