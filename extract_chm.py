import os
from bs4 import BeautifulSoup
import chm

def extract_chm_to_text(chm_path, out_path):
    """
    Extracts text from a CHM file and saves it to a text file.
    """
    try:
        book = chm.CHMFile(chm_path)
    except Exception as e:
        print(f"❌ Failed to open {chm_path}: {e}")
        return

    all_text = f"\n=== Start of {chm_path} ===\n"

    for file in book.files:
        if file.lower().endswith((".html", ".htm")):
            try:
                data = book.read_file(file)
                if data:
                    soup = BeautifulSoup(data, "html.parser")
                    text = soup.get_text(separator="\n")
                    all_text += f"\n--- {file} ---\n{text}\n"
            except Exception as e:
                print(f"⚠️ Error reading {file}: {e}")

    all_text += f"\n=== End of {chm_path} ===\n"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(all_text)

    print(f"✅ Extracted {chm_path} → {out_path}")

def main():
    chm_files = [f for f in os.listdir(".") if f.lower().endswith(".chm")]

    if not chm_files:
        print("No CHM files found in the current folder.")
        return

    print(f"Found {len(chm_files)} CHM file(s): {chm_files}")

    for chm_file in chm_files:
        txt_file = chm_file.rsplit(".", 1)[0] + ".txt"
        extract_chm_to_text(chm_file, txt_file)

if __name__ == "__main__":
    main()
