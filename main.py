import fitz
import csv
import os
import glob
import sys


def extract_data_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    extracted_data = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        page_text = page.get_text()
        lines = page_text.split("\n")

        segment = None
        id_liste_de_controle = None
        number_of_ring = None

        for i in range(len(lines)):
            if lines[i].strip() == "installé":
                segment = lines[i + 1].strip()
            if lines[i].strip() == "création":
                id_liste_de_controle = lines[i + 1].strip()
            if "Numéro de l'anneau / Number of the ring" in lines[i].strip():
                number_of_ring = lines[i + 1].strip()
                if segment and id_liste_de_controle and number_of_ring:
                    extracted_data.append(
                        [
                            segment,
                            id_liste_de_controle,
                            number_of_ring,
                            os.path.basename(pdf_path),
                        ]
                    )
                    segment = None
                    id_liste_de_controle = None
                    number_of_ring = None

    document.close()
    return extracted_data


def save_to_csv(data, csv_path):
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Segment installé",
                "ID de liste de contrôle",
                "Numéro de l'anneau",
                "Fichier",
            ]
        )
        writer.writerows(data)


def find_pdf_files(directory):
    return glob.glob(os.path.join(directory, "**", "*.pdf"), recursive=True)


def main():
    if getattr(sys, "frozen", False):
        directory = os.path.dirname(sys.executable)
    else:
        directory = os.path.dirname(os.path.realpath(__file__))

    csv_path = os.path.join(directory, "output.csv")
    all_extracted_data = []

    pdf_files = find_pdf_files(directory)
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}")
        data = extract_data_from_pdf(pdf_file)
        all_extracted_data.extend(data)

    save_to_csv(all_extracted_data, csv_path)
    print(f"Data extracted and saved to {csv_path}")


if __name__ == "__main__":
    main()
