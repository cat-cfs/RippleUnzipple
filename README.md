# Ripple Unzipple

## Project Description

The Ripple Unzipple project is a Python script designed to recursively unzip all compressed folders in a given directory. It supports both .zip and .7z file formats and provides a straightforward solution for efficiently extracting compressed data. The script is particularly useful for scenarios where nested compressed folders need to be extracted.

## Table of Contents

- [Project Description](#project-description)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install and set up Ripple Unzipple, follow these steps:

1. Clone the repository to your local machine.
2. Ensure that you have Python 3 installed.
3. Install the required dependencies using the following command:

```
pip install -r /path/to/requirements.txt
```

## Usage

To use Ripple Unzipple, run the script from the command line with the following syntax:
```
python ripple_unzipple.py input_path output_path [log_path]
```
- input_path: Path to the input directory or compressed file.
- output_path: Path to the output directory where the uncompressed data will be stored.
- log_path (optional): Path to the log file. If provided, detailed logs will be saved to this file.

Example:
```
python ripple_unzipple.py /Testing/Data/TestFolder.zip /OutputFolder OutputLogs.txt
```

You also have the option of calling this function from a module import with the following syntax:
```
from /path/to/ripple_unzipple import ripple_unzip

def main():
    ripple_unzip('input_path', 'output_path', 'log_path')
```

## Configuration

No specific configuration is required for Ripple Unzipple. However, you can customize the script's behavior by adjusting the input parameters during execution.

## Contributing

Although this project will most likely not be maintained or anything.

If you would like to contribute to Ripple Unzipple, follow these guidelines:

1. Submit bug reports or feature requests via the GitHub issue tracker.
2. Fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

If you have any questions, feedback, or suggestions, you can reach out here:

- Anthony Rodway
- Email: anthony.rodway@nrcan-rncan.gc.ca

Feel free to provide your input to help improve Ripple Unzipple!

