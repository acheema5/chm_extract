import os
from bs4 import BeautifulSoup

# Path to the folder containing all CHM subfolders
ROOT_FOLDER = "."  # current folder

def html_to_text(html_path):
    """Read HTML file and return clean text"""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text(separator="\n")
            # Optional: remove extra blank lines
            text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
            return text
    except Exception as e:
        print(f"⚠️ Error reading {html_path}: {e}")
        return ""

def process_chm_folder(folder_path):
    """Convert all HTML files in a folder to one TXT file"""
    folder_name = os.path.basename(folder_path)
    output_file = os.path.join(ROOT_FOLDER, folder_name + ".txt")
    combined_text = f"=== Text from {folder_name} ===\n"

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".html", ".htm")):
                html_path = os.path.join(root, file)
                combined_text += f"\n--- {file} ---\n"
                combined_text += html_to_text(html_path) + "\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(combined_text)
    print(f"✅ Converted {folder_name} → {output_file}")

def main():
    # Find all CHM subfolders in ROOT_FOLDER
    for item in os.listdir(ROOT_FOLDER):
        item_path = os.path.join(ROOT_FOLDER, item)
        if os.path.isdir(item_path):
            process_chm_folder(item_path)

if __name__ == "__main__":
    main()
