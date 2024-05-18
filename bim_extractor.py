import fitz
import csv
import os
import glob
import sys
import concurrent.futures
import time


def format_id(id):
    return f"BIM{id[-4:]}_404100"


def extract_data_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    extracted_data = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        lines = page.get_text("text").split("\n")

        segment = None
        id_liste_de_controle = None
        number_of_ring = None

        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line == "installé":
                segment = lines[i + 1].strip()
            elif stripped_line == "création":
                id_liste_de_controle = format_id(lines[i + 1].strip())
            elif "Numéro de l'anneau / Number of the ring" in stripped_line:
                number_of_ring = lines[i + 1].strip()
                if segment and id_liste_de_controle and number_of_ring:
                    extracted_data.append(
                        [
                            number_of_ring,
                            segment,
                            id_liste_de_controle,
                            os.path.basename(pdf_path),
                        ]
                    )
                    segment = id_liste_de_controle = number_of_ring = None

    document.close()
    print(f"Processed {pdf_path}")
    return extracted_data


def save_to_csv(data, csv_path):
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Numéro de l'anneau",
                "Segment installé",
                "ID de liste de contrôle",
                "Fichier",
            ]
        )
        writer.writerows(data)


def find_pdf_files(directory):
    return glob.glob(os.path.join(directory, "**", "*.pdf"), recursive=True)


def main():
    start_time = time.time()

    if getattr(sys, "frozen", False):
        directory = os.path.dirname(sys.executable)
    else:
        directory = os.path.dirname(os.path.realpath(__file__))

    csv_path = os.path.join(directory, "output.csv")
    all_extracted_data = []

    pdf_files = find_pdf_files(directory)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(extract_data_from_pdf, pdf_files))

    for result in results:
        all_extracted_data.extend(result)

    save_to_csv(all_extracted_data, csv_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Data extracted and saved to {csv_path}")
    print(f"Total execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
