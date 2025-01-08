import json 
from google import generativeai as genai


class Summarizer:
    
    def __init__(self):
        genai.configure(api_key="API_KEY")
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def generate_summary(self,paper,conference):
 
        if conference == "nan":
            conference_info = "Conference: nan"
        else:
            conference_info = f"Conference Type: {conference}"
        
        return self.model.generate_content(
             f"""
        Please summarize this research paper concisely, ensuring all existing sections such as Title, Abstract, Introduction, Methodology, Results, and Conclusion are included. 
        Keep the summary detailed but not overly long, summarizing each section individually while preserving key information. 
        Do not attempt to complete or add missing sections, and avoid mentioning missing sections explicitly. 
        Additionally, provide a brief description of how the sections relate to each other and at last add a section to specify the conference type from the research paper conference key just give the name if its 'no conference' just keep it as 'no conference' and dont add any other text or explanantion there.
        
        {paper}
        
        {conference_info}
        
        """
        ).text



if __name__=='__main__':
    Summarizer()