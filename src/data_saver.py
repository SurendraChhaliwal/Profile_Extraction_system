import os
import json
import pandas as pd

def save_json(output_path,file_name, data):
    os.makedirs(output_path,exist_ok=True)
    file_path = os.path.join(output_path,file_name)
    with open(file_path,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=4)

def parse_and_save(output_path, file_name, data):
    os.makedirs(output_path,exist_ok=True)
    df = pd.DataFrame(data)
    destination = os.path.join(output_path, f"{file_name}.xlsx")
    df.to_excel(destination, index= False)

def save_run_logs(outtput_path, log_file_name,run_details):
    os.makedirs(outtput_path,exist_ok=True)
    log_path = os.path.join(outtput_path,log_file_name)
    with open(log_path,'w',encoding='utf-8') as f:
        f.write("# LOGS\n\n")
        f.write("Resume Extraction Pipeline\n\n")
        f.write(f"**Run ID:** {run_details['run_id']}\n")
        f.write(f"**Date:** {run_details['date']}\n")
        f.write(f"**Provider:** {run_details['provider']}\n")
        f.write(f"**Model:** {run_details['model']}\n")
        f.write(f"**Total Resumes:** {run_details['total']}\n")
        f.write(f"**Successful:** {run_details['successful']}\n")
        f.write(f"**Failed:** {run_details['failed']}\n")
        f.write(f"\n**Execution Time:** {run_details['execution_time']}\n")
        f.write(f"\n**Status:** {run_details['status']}\n")