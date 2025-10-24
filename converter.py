import os
from bs4 import BeautifulSoup

def html_to_text(html_path):
    """Convert HTML to plain text, with encoding fallbacks"""
    for encoding in ["utf-8", "windows-1252"]:
        try:
            with open(html_path, "r", encoding=encoding) as f:
                soup = BeautifulSoup(f, "html.parser")
                text = soup.get_text(separator="\n")
                # Remove extra blank lines
                text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
                return text
        except Exception:
            continue
    print(f"Failed to read {html_path} with utf-8 and windows-1252")
    return ""

def convert_html_folder_to_txt(input_folder, output_file):
    """Combine all HTML/HTM files from a folder into one text file"""
    print(f"\n Processing folder: {input_folder}")
    all_texts = []

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith((".html", ".htm")):
                html_path = os.path.join(root, file)
                try:
                    text = html_to_text(html_path)
                    if text:
                        rel_path = os.path.relpath(html_path, input_folder)
                        all_texts.append(f"\n=== {rel_path} ===\n{text}")
                except Exception as e:
                    print(f"Error reading {html_path}: {e}")

    if all_texts:
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("\n\n".join(all_texts))
        print(f"✅ Wrote {len(all_texts)} files to {output_file}")
    else:
        print(f"No HTML files found in {input_folder}")

if __name__ == "__main__":
    base_dir = r"C:\Users\arjun\extractor\chm_extract"

    folders = [
        os.path.join(base_dir, "AppLevel"),
        os.path.join(base_dir, "VbaLevel"),
        os.path.join(base_dir, "SysLevel")
    ]

    for folder in folders:
        if os.path.exists(folder):
            output_name = os.path.basename(folder) + "_combined.txt"
            output_path = os.path.join(base_dir, output_name)
            convert_html_folder_to_txt(folder, output_path)
        else:
            print(f"Folder not found: {folder}")
