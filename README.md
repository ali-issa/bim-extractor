# PDF Data Extractor

This script extracts specific data from all PDF files in the working directory and its subdirectories and saves the extracted data into a CSV file. The extracted data includes the "Segment installé", "ID de liste de contrôle", and "Numéro de l'anneau", along with the file name from which the data was extracted.

## Features

- Traverses the working directory and all subdirectories to find PDF files.
- Extracts the "Segment installé", "ID de liste de contrôle", and "Numéro de l'anneau" from each PDF.
- Saves the extracted data into a CSV file named `output.csv`.
- The CSV file includes a column for the file name from which the data was extracted.

## Requirements

- Python 3.x
- PyMuPDF
- PyInstaller

## Installation

1. **Clone or download the repository**:

```bash
git clone https://github.com/ali-issa/bim-extractor.git
cd bim-extractor
```

2. **Install the required Python packages**:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Script

You can run the script directly using Python:

```bash
python extractor.py
```

### Building the Executable

To distribute the script as an executable file for non-technical users, you can use PyInstaller to create a standalone binary. Follow these steps:

1. **Build the executable**:

```bash
pyinstaller --onefile --windowed extractor.py
```

The executable will be created in the `dist` directory. Distribute the executable file (`extractor` or `extractor.exe` on Windows) to users. They can run it by double-clicking the file.

## Notes

- Ensure that all the PDF files you want to process are located in the same directory as the executable or in its subdirectories.
- The output CSV file, `output.csv`, will be created in the same directory as the executable.
