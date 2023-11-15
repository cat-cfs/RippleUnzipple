#!/usr/bin/env python3
#~-~ encoding: utf-8 ~-~
# ripple_unzipple/ripple_unzipple.py
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
File: ripple_unzipple/ripple_unzipple.py
Created By:       Anthony Rodway
Email:            anthony.rodway@nrcan-rncan.gc.ca
Creation Date:    Fri November 10 14:00:00 PST 2023
Organization:     Natural Resources of Canada
Team:             Carbon Accounting Team

Description: 
    Recursively unzips all compressed folders in a given directory.

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
from distutils.dir_util import copy_tree


#========================================================
# Global Classes
#========================================================
# ANSI escape codes for colors
class Colors:
    ERROR = '\033[91m' # red
    WARNING = '\033[93m' # yellow
    INFO = '\033[94m' # blue
    END = '\033[0m'
      

#========================================================
# Logging
#========================================================   
def logging(file_path, type, message):
    """
    Log messages with colored tags and timestamps.

    Args:
        file_path (str): Path to the log file.
        type (str): Color code for the log message type.
        message (str): The log message.
        
    Return:
        None.
    """
    # Set the tag, 'ERROR' is default.
    tag = 'ERROR'
    if type == Colors.INFO:
        tag = 'INFO'
    elif type == Colors.WARNING:
        tag = 'WARNING'
        
    # Print the colored log message to the console
    print(f'{type}[{tag}] {message}{Colors.END}')
    
    # If there is a file path provided
    if file_path != '':
        # Open the file in append mode and append a log message
        with open(file_path, 'a') as log_file:
            log_file.write(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} [{tag}] {message}\n')
    

#========================================================
# Unzipping Functions
#========================================================
def ripple_unzip(input_path, output_path, log_path = ''):
    """
    Unzip .zip and .7z files either for a directory or a compressed file.

    Args:
        input_path (str): Path to the input directory or compressed file.
        output_path (str): Path to the output directory.
        log_path (str, optional): Path to the log file. Defaults to ''.
        
    Return:
        None.
    """
    try:
        # Check if the provided path exists
        if not os.path.exists(input_path):
            raise ValueError(f"The specified path does not exist: {input_path}")
        
        # Handle different input extensions
        if os.path.isdir(input_path):
            # First copy the directory to the new location 
            copy_tree(input_path, output_path)
            recursive_unzip(input_path, output_path)
        
        elif input_path.endswith((".zip", ".7z")):
            os.makedirs(output_path, exist_ok=True)

            with ZipFile(input_path, mode='r') if input_path.endswith(".zip") else SevenZipFile(input_path, mode='r') as archive_ref:
                archive_ref.extractall(output_path)
                recursive_unzip(output_path, output_path)
        
        else:
            raise ValueError("Unsupported input type. Please provide a directory or a compressed file.")
        
    except ValueError as error:
        logging(log_path, Colors.ERROR, str(error))
        raise ValueError(error)   
    except Exception as error:
        logging(log_path, Colors.ERROR, str(error))
        raise Exception(error)  
    
def recursive_unzip(input_path, output_path):   
    """
    Recursively unzip .zip and .7z files in the input_path to the output_path.

    Args:
        input_path (str): Path to the input directory or compressed file.
        output_path (str): Path to the output directory.
        
    Return:
        None.
    """
    # Create output_path if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Iterate through the directory and unzip any compressed folders
    for root, dirs, files in os.walk(input_path):
        for file in files:
            # Get the file path of the input 
            file_path = os.path.join(root, file)
            
            # Get the path that the file will be extracted to
            extract_path = os.path.join(output_path, os.path.splitext(file_path)[0][len(input_path) + 1:])

            file_to_remove = ''
            if file.endswith((".zip", ".7z")):
                with ZipFile(file_path, mode='r') if file.endswith(".zip") else SevenZipFile(file_path, mode='r') as archive_ref:
                    archive_ref.extractall(extract_path)
                    
                    # Recursively call the function to check every file in the directory tree
                    recursive_unzip(extract_path, extract_path)
                    
                    # Flag the compressed file to be removed
                    file_to_remove = extract_path + '.zip' if file.endswith(".zip") else extract_path + '.7z'

                # Remove the original compressed file from the new output folder
                os.remove(file_to_remove)

            
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
        log_path = ''
        if len(sys.argv) == 4:
            ripple_unzip(sys.argv[1], sys.argv[2], sys.argv[3])
            log_path = sys.argv[3]

        # Call the main logic function for starting the recursive unzipping
        ripple_unzip(sys.argv[1], sys.argv[2])
    except Exception as error:
        # logging(log_path, Colors.ERROR, error)
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
    