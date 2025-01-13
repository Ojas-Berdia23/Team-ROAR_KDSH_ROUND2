import csv 
import os
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score



def get_test_data(path):
    all_files = []
    try:
        
        for root, dirs, files in os.walk(path):
            if files:  # Ensure there are files in the directory
                # Determine if the file is from Non-Publishable or Publishable
                if "Non-Publishable" in root:
                    p_type = "0"
                    conference = "na"
                else:
                    p_type = "1"
                    # Extract the conference name from the folder name
                    conference = os.path.basename(root).lower()
                for file in files:
                    if file.endswith(".pdf"):  # Assuming research papers are PDF files
                        with open('../test.csv','a',newline='',encoding='UTF-8') as csvfile:
                            writer = csv.writer(csvfile)
                            if csvfile.tell()==0:
                                writer.writerow(['Paper ID', 'Publishable_ACTUAL', 'Conference_ACTUAL'])
                            writer.writerow([file[:-4],p_type,conference])
            else:
                print("file not found")
                        
    except Exception  as e:
        print(e)              
    
    
def validate():
    test_data = pd.read_csv("../test.csv")
    prediction_data = pd.read_csv("../prediction.csv").drop(columns=['Rationale'])
    
    data = pd.DataFrame(pd.merge(test_data,prediction_data,on='Paper ID'))
    
    publishable_accuracy = accuracy_score(data["Publishable_ACTUAL"], data["Publishable"])
    publishable_f1 = f1_score(data["Publishable_ACTUAL"], data["Publishable"])
    conference_accuracy = (data["Conference_ACTUAL"] == data["Conference"]).mean()

    print(data)
    # with open(file,'w') as f:
        
if __name__=='__main__':
    
    
    # get_test_data("../KDSH_2025_Dataset/Reference")
    # print("done getting file info")
    
    validate()
    
    