import os
import time
from pathlib import Path
from datetime import datetime

from src.data_loader import load_data
from src.models import ScreenResume
from src.prompt_builder import system_prompt, build_prompt
from src.llm_client import call_llm
from src.retry_handler import call_with_retry
from src.data_saver import (save_json,save_run_logs,parse_and_save)

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
print(f"Run ID : {run_id}")

def Processor(config):
    # Start execution timer
    start_time = time.perf_counter()
    run_date = datetime.now().astimezone().strftime('%Y-%m-%d')

    errors=[]
    data=[]
    processed=[]

    source_path = config['input']['source_path']
    output_path = config['output']['output_path']
    raw_path = config['output']['raw_response']
    parsed_path = config['output']['parsed_response']

    provider = config['llm']['provider']
    model = config['llm']['model']
    client = config['client']

    max_attempts = config['retry']['max_attempts']
    initial_delay = config['retry']['initial_delay']
    max_delay = config['retry']['max_delay']

    # Create output folders
    os.makedirs(output_path,exist_ok=True)
    os.makedirs(raw_path,exist_ok=True)
    os.makedirs(parsed_path,exist_ok=True)

    #Get/load the resumes
    resume_files = sorted(
        Path(source_path).glob(f"*.txt")
    )

    if not resume_files:
        raise FileNotFoundError("No resume are found!")

    # Process resumes
    for file_path in resume_files:
        cand_id = file_path.stem
        print(f"\n Processing ID: {cand_id}")
        processed.append(cand_id)
        try:
            # Load resume
            text = load_data(file_path=file_path)

            # Build prompt
            user_prompt = build_prompt(resume_text=text)

            # Call api with query
            response = call_with_retry(
                api_function=call_llm,
                client=client,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=ScreenResume,
                model=model,
                max_attempts=max_attempts,
                initial_delay=initial_delay,
                max_delay=max_delay
            )

            # Save raw api response
            raw_dump = response.model_dump(mode='json')

            save_json(output_path=raw_path, file_name=f"{cand_id}_raw.json",data=raw_dump)

            # Extract parsed response
            parsed_obj = response.choices[0].message.parsed

            if parsed_obj is None:
                raise ValueError("Parsed response is empty")

            parsed_dump = parsed_obj.model_dump(mode='json')

            # save parsed response in json format seperately
            save_json(output_path=parsed_path, file_name=f"{cand_id}_parsed.json",data=parsed_dump)

            parsed_dump['cand_id'] = cand_id

            data.append(parsed_dump)

            print(f"Successfully processed: {cand_id}")

        except Exception as e:
            print(f"Error in {cand_id}: {e}")

            errors.append({'candidate_id': cand_id,
                           'error':str(e)})

    # Export to excel
    export_error = None

    try:
        print("\n Saving excel output")
        parse_and_save(output_path=output_path,file_name=f"results_{run_id}",data=data)
        parse_and_save(output_path=output_path,file_name=f"errors_{run_id}",data=errors)
    except Exception as e:
        export_errors= str(e)
        print(f"Errors while saving the excel files: {e}")

    # Calculate total execution time
    end_time = time.perf_counter()

    total_minutes = round((end_time - start_time)/60,2)

    # Prepare run detail
    run_details = {
        'run_id':run_id,
        'date':run_date,
        'provider':provider,
        'model':model,
        'total':len(processed),
        'successful':len(data),
        'failed':len(errors),
        'execution_time':f"{total_minutes} minutes",
        'status':'successful' if export_error is None else 'failed'
    }

    # Save Logs
    print("Saving logs....")
    save_run_logs(outtput_path=output_path,log_file_name=f"logs_{run_id}.md",run_details=run_details)

    print("\nPipeline is completed !....")

    print(f"Total resume processed: {run_details['total']}")
    print(f"Successful: {run_details['successful']}")
    print(f"Falied: {run_details['failed']}")
    print(f"Execution time: {run_details['execution_time']}")

    if export_error:
        raise RuntimeError(f"Failed to save the excel: {export_error}")

