import json
from google import generativeai as genai

class Summarizer:
    def __init__(self):
        genai.configure(api_key="API_KEY")
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def make_prediction(self, paper):
        return self.model.generate_content(
            f"""
            You are tasked with evaluating a research paper and determining whether it is **Publishable** or **Non-Publishable**. Additionally, if the paper is **Publishable**, you must recommend the most suitable conference from the following list:of coferences **CVPR**, **NeurIPS**, **DAA**, **EMNLP**, **TMLR**,**KDD**.

            ### Instructions:
            1. **Classify the paper**:
                - If **Non-Publishable**, return:
                  - `"status": "non-publishable"`
                  - `"type": "na"`
                  - `"reason": "<brief explanation of why it's non-publishable>"` (no more than 100 words). This may include lack of novelty, poor methodology, insufficient data, or irrelevance.

                - If **Publishable**, return:
                  - `"status": "publishable"`
                  - `"type": "<conference name (CVPR, NeurIPS, DAA, EMNLP, TMLR, KDD)>"`
                  - `"reason": "<short explanation of why it fits the conference, no more than 100 words>"`. This includes relevance to the field, novelty, technical rigor, or alignment with the conference's scope.

            ### Example Conference Types and Descriptions:
            - **CVPR**: Focuses on Computer Vision, Image Processing, and related topics.
            - **NeurIPS**: Covers Machine Learning, Artificial Intelligence, and related disciplines.
            - **DAA**: Specializes in Data Science and Algorithms.
            - **EMNLP**: Focuses on Natural Language Processing and related research.
            - **TMLR**: Deals with Machine Learning theory and research.
            - **KDD**: Focuses on Knowledge Discovery and Data Mining.

            ### Example Responses:
            For a **Publishable** paper:
            ```json
            {{
                "status": "publishable",
                "type": "CVPR",
                "reason": "Introduces a novel approach to 3D image recognition, fitting CVPR's focus on computer vision."
            }}
            ```

            For a **Non-Publishable** paper:
            ```json
            {{
                "status": "non-publishable",
                "type": "na",
                "reason": "The paper lacks original contributions and sufficient experimental validation."
            }}
            ```

            ### Research Paper Text:
            {paper}
            """
        ).text
