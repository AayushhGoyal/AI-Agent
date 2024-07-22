import google.generativeai as genai
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import time
import os

# Configure logging to console and file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger('').addHandler(console_handler)
logging.FileHandler(r"C:\Users\Ayush Goyal\OneDrive\Desktop\AI agent2\duplicate_data_20_entries.csv")

# Replace with your actual OpenAI API key
genai.configure(api_key='AIzaSyA-s-XT2oiP13SuOdE4Q1-NSU9PB105rgc')

def use_llama2_to_explain(discrepancy):
    prompt = f"Explain the following data discrepancy: {discrepancy}"
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Error using Llama2 to explain discrepancy: {e}")
        return None

def describe_csv_columns(file_path):
    try:
        df = pd.read_csv(file_path)
        column_descriptions = []
        content = df.head(2).to_string()
        
        prompt = f"Describe the columns of this csv file '{content}'."
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        # column_descriptions.append(f"{content}: {response.text}")
        
        # response = "\n".join(column_descriptions)
        logging.info(f"CSV Column Descriptions:\n{response.text}")
        return response.text
    except Exception as e:
        logging.error(f"Error describing columns in {file_path}: {e}")
        return None

class FileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            logging.info(f"File modified: {event.src_path}")
            check_file_for_discrepancies(event.src_path)

def remove_duplicates(df, file_path):
    try:
        df_cleaned = df.drop_duplicates()
        df_cleaned.to_csv(file_path, index=False)
        logging.info(f"Duplicates removed and file updated: {file_path}")
    except Exception as e:
        logging.error(f"Error removing duplicates from {file_path}: {e}")

def check_file_for_discrepancies(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Check for duplicates
        if df.duplicated().any():
            discrepancy = "Duplicate data found"
            logging.warning(f"{discrepancy} in {file_path}")
            explanation = use_llama2_to_explain(discrepancy)
            logging.info(f"Llama2 Explanation: {explanation}")
            remove_duplicates(df, file_path)
        
        # Check for missing values
        if df.isnull().values.any():
            discrepancy = "Missing values found"
            logging.warning(f"{discrepancy} in {file_path}")
            explanation = use_llama2_to_explain(discrepancy)
            logging.info(f"Llama2 Explanation: {explanation}")
        
        # Describe columns
        describe_csv_columns(file_path)
        
        # More complex checks can be added here
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    path = r"C:\Users\Ayush Goyal\OneDrive\Desktop\AI agent2"
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    logging.info("Started monitoring the directory for changes.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    logging.info("Stopped monitoring the directory.")
