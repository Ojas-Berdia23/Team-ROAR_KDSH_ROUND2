import json
import fitz
import os
import csv
from summarizer import Summarizer
import re


summary_model = Summarizer()

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

def predict(text):
    try:
        summary_content = summary_model.make_prediction(text)
        start = summary_content.index('{')
        end = summary_content.index('}')
        print('summary',summary_content[start:end+1])

        summary_content = summary_content[start:end+1]
        
        # Log the model output before parsing
        
        # Parse the summary content (expected to be a JSON string) into a dictionary
        prediction = json.loads(summary_content)

        # Extract the status, type (conference), and reason from the prediction
        status = 1 if prediction.get('status') == "publishable" else 0
        conference = prediction.get('type', 'na').lower()
        rationale = prediction.get('reason', 'na')
        return [status,conference,rationale]
    
    except Exception as e:
        print(f"Error while making prediction for file {e}")

def make_prediction(file, csv_file):
    content_path = file['file_path']
    paper_content = get_text_from_pdf(content_path)
    
    try:
        summary_content = summary_model.make_prediction(paper_content)
        start = summary_content.index('{')
        end = summary_content.index('}')
        print('summary',summary_content[start:end+1])

        summary_content = summary_content[start:end+1]
        
        # Log the model output before parsing
        print(f"Model output for {file['file_name']}: {summary_content}")
        
        # Parse the summary content (expected to be a JSON string) into a dictionary
        prediction = json.loads(summary_content)

        # Extract the status, type (conference), and reason from the prediction
        status = 1 if prediction.get('status') == "publishable" else 0
        conference = prediction.get('type', 'na').lower()
        rationale = prediction.get('reason', 'na')

        # Using file['file_name'] as paper_id
        paper_id = file['file_name'][:-4] # This assigns the paper's filename as its ID

        # Append the prediction to the CSV file
        with open(csv_file, 'a', newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Ensure header is written only once
            if csvfile.tell() == 0:
                writer.writerow(['Paper ID', 'Publishable', 'Conference', 'Rationale'])

            writer.writerow([paper_id, status, conference, rationale])
            print(f'Prediction written for {file["file_name"]}')
    except Exception as e:
        print(f"Error while making prediction for {file['file_name']}: {e}")



if __name__ == '__main__':
    data_path = "../KDSH_2025_Dataset/Papers"
    result_csv_path = "../result.csv"
    prediction_data_path = "../KDSH_2025_Dataset/Reference"
    prediction_csv_path = '../prediction.csv'
    
    # Get list of files
    files = get_files(data_path)
    
    
    # prediction_file = get_files(prediction_data_path)
    
    
    # for cross validation 
    # for file in prediction_file:
        # make_prediction(file,prediction_csv_path)
    
    # Process each file and generate predictions
    for file in files:
        make_prediction(file, result_csv_path)
