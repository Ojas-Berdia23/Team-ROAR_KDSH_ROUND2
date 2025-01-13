import json
import fitz
import os
from summarizer import Summarizer




def get_text_from_pdf(path):
    try:
        with fitz.open(path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()  # This returns text, no need for get_textpage()
        return text
    except Exception as e:
        print(f"Error: {e}")


def get_files(base_path):
    # Walk through all directories and subdirectories
    # Function gets the file_path, file_name, dir_name
    # Returns a list of file objects
    
    all_files = []
    for root, dirs, files in os.walk(base_path):
        if files:  # Ensure there are files in the directory
            # Determine if the file is from Non-Publishable or Publishable
            if "Non-Publishable" in root:
                p_type = "non-publishable"
                conference = "no conference"
            else:
                p_type = "publishable"
                # Extract the conference name from the folder name
                conference = os.path.basename(root)

            for file in files:
                if file.endswith(".pdf"):  # Assuming research papers are PDF files
                    all_files.append({
                        "p_type": p_type,
                        "conference": conference,
                        "file_path": os.path.join(root, file),
                        "file_name": file
                    })
    return all_files


def create_summary_file(file):
    file_type = file['p_type']
    file_name = f"{file['file_name']}.txt"
    content_path = file['file_path']
    paper_content = get_text_from_pdf(content_path)
    conference = file['conference']
    if not os.path.exists(summary_path):
        os.mkdir('../summaries')

    if not os.path.exists('../summaries/Non-publishable') and not os.path.exists('../summaries/Publishable'):
        os.makedirs(os.path.join(summary_path, "Publishable"), exist_ok=True)
        os.makedirs(os.path.join(summary_path, "Non-publishable"), exist_ok=True)

    if file_type == 'publishable':
        dir = os.path.join(summary_path, 'Publishable')
    else:
        dir = os.path.join(summary_path, 'Non-publishable')

    os.makedirs(dir, exist_ok=True)

    file_path = os.path.join(dir, file_name)

    if os.path.exists(file_path):
        print(f'File: "{file_path}" Exist')
    else:
        try:
            summary_content = summary_model.generate_summary(paper_content,conference)
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write(summary_content)
                print('File written')
        except Exception as e:
            print(f'{e} Occurred')


if __name__ == '__main__':
    
    data_path = "../KDSH_2025_Dataset/Reference"
    summary_path = "../summaries"
    files = get_files(data_path)
    summary_model = Summarizer()
    for file in files:
        create_summary_file(file)
