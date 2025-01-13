# Team ROAR

The manual evaluation of research papers for conference submission is a labor-intensive and subjective process. This project addresses this challenge by developing AI-driven systems using advanced language models, comparative analysis techniques, and real-time data frameworks. The proposed solution involves two major tasks:

Research Paper Publishability Assessment: Classifying research papers as "Publishable" or "Non-Publishable" based on quality and content.

Conference Selection: Recommending suitable conferences for "Publishable" papers with a formal justification.

## Installation

1. Install all the dependency by running:

   ```bash
   pip install -r requirements.txt
   ```
2. Set the Gemini API key:

   ```bash
   export GOOGLE_GEMINI_API_KEY=your_api_key  # For Linux/Mac
   set GOOGLE_GEMINI_API_KEY=your_api_key    # For Windows
   ```

## Running the Project

1. Ensure the API_KEY is set.
2. Run the preprocess file to generate the results in the results.csv file :

   ```bash
   python preprocess.py
   ```
3. Run the predict file to create Web UI for prediction

   ```
   streamlit run predict.py
   ```
4. Run validation file to get the Accuracy and F1 Score in the accuracy.txt file:

   ```
   python validate.py
   ```
