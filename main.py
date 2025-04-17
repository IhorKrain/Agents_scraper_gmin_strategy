import os
import sys
from pathlib import Path
from crew.crew import crew
from rag.qa_chain import load_vectorstore_from_pdf

PDF_DIR = "pdfs"

def list_pdf_files():
    pdfs = list(Path(PDF_DIR).glob("*.pdf"))
    if not pdfs:
        print("❌ Nie znaleziono żadnych plików PDF w katalogu:", PDF_DIR)
        sys.exit(1)

    print("📄 Dostępne pliki PDF:")
    for idx, pdf in enumerate(pdfs):
        print(f"{idx + 1}. {pdf.name}")
    return pdfs

def choose_pdf(pdfs):
    choice = input("\nWybierz numer pliku do analizy: ")
    try:
        idx = int(choice) - 1
        return str(pdfs[idx])
    except (ValueError, IndexError):
        print("❌ Niepoprawny wybór.")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Analiza strategii rozwoju gminy na podstawie dokumentu PDF\n")
    pdf_files = list_pdf_files()
    selected_pdf = choose_pdf(pdf_files)

    print(f"\n📂 Wybrany plik: {selected_pdf}\n")

    # 🔄 Wczytaj dokument do RAG
    load_vectorstore_from_pdf(selected_pdf)

    # 🚀 Uruchom analizę przez CrewAI
    result = crew.kickoff(inputs={"pdf_path": selected_pdf})

    print("\n✅ Wynik końcowy:")
    print(result)
