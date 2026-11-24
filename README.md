# Profile Extraction System

A Python pipeline that reads resume text files, sends each resume to an OpenAI model, and extracts structured candidate information. Results are exported to Excel, with separate JSON files for raw and parsed API responses.

## Features

- Processes all `.txt` resume files in `data/resumes/`
- Extracts candidate name, contact details, location, experience, job title, company, education, and notice period
- Returns grounded answers with reasoning for each extracted field
- Retries retryable OpenAI API errors with exponential backoff
- Exports successful results to an Excel workbook
- Exports failed candidates to a separate Excel workbook
- Writes raw responses, parsed responses, and run logs

## Extracted Fields

The pipeline returns:

- Candidate ID
- Name and name reasoning
- Email and email reasoning
- Phone number and phone reasoning
- Current location and location reasoning
- Total experience and reasoning
- Relevant experience and reasoning
- Current job title and title reasoning
- Current company and company reasoning
- Highest education and education reasoning
- Notice period and notice-period reasoning

## Project Structure

```text
Profile_Extraction_system/
├── config/
│   └── config.yaml
├── data/
│   └── resumes/          # Resume .txt files
├── .vscode/
│   └── settings.json
├── pyproject.toml       # Ruff configuration
├── src/
│   ├── config_loader.py
│   ├── data_loader.py
│   ├── data_saver.py
│   ├── llm_client.py
│   ├── models.py
│   ├── processor.py
│   ├── prompt_builder.py
│   └── retry_handler.py
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- An OpenAI API key with access to the configured model
- Internet access

## Setup

### 1. Clone the repository

```powershell
git clone <your-github-repository-url>
cd Profile_Extraction_system
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The requirements include `python-dotenv` for loading credentials from `.env` and Ruff for formatting and linting.

### 4. Configure the API key

Create a `.env` file in the project root:

```dotenv
OpenAPI_Paid_Key=your-openai-api-key
```

The variable name is controlled by `config/config.yaml`. Do not commit `.env`; it is already excluded by `.gitignore`.

### 5. Configure the pipeline

Edit `config/config.yaml` as needed:

```yaml
input:
  source_path: data/resumes

output:
  output_path: output
  raw_response: raw_response
  parsed_response: parsed_response

llm:
  api_key: "OpenAPI_Paid_Key"
  provider: openai
  model: gpt-4o-mini

retry:
  max_attempts: 3
  initial_delay: 2
  max_delay: 30
```

`api_key` is the environment-variable name, not the API key itself.

## Running the Pipeline

Place UTF-8 `.txt` files in `data/resumes/` and run:

```powershell
python main.py
```

For example:

```text
data/resumes/CAND001.txt
data/resumes/CAND002.txt
```

## Output

Each run creates the following files under `output/`:

```text
output/
├── raw_response/
│   └── CAND001_raw.json
├── parsed_response/
│   └── CAND001_parsed.json
├── results_<run-id>.xlsx
├── errors_<run-id>.xlsx
└── logs_<run-id>.md
```

- `raw_response/` contains the complete OpenAI response objects.
- `parsed_response/` contains only the structured Pydantic data.
- `results_<run-id>.xlsx` contains successfully parsed candidates.
- `errors_<run-id>.xlsx` contains candidates that failed processing.
- `logs_<run-id>.md` contains run totals and execution details.

## Formatting and Linting

Ruff configuration is stored in `pyproject.toml`. Format Python source files with:

```powershell
ruff format .
```

Check formatting without changing files:

```powershell
ruff format --check .
```

Run lint checks with:

```powershell
ruff check .
```

Apply safe Ruff lint fixes with:

```powershell
ruff check --fix .
```

VS Code can format Python files on save when the Ruff extension is installed:

1. Open Extensions with `Ctrl+Shift+X`.
2. Install **Ruff** by Astral Software.
3. Open a `.py` file and save it to format automatically.

## Privacy and GitHub Usage

Resume files and extracted results can contain names, email addresses, phone numbers, employment history, and other personal data.

Before pushing to GitHub:

- Never commit `.env` or API credentials.
- Review `data/resumes/` and remove personal or sample resumes before publishing.
- Review generated `output/`, `raw_response/`, and `parsed_response/` folders for sensitive data.
- Add or verify ignore rules for private data and generated results.

## Notes

- Only UTF-8 `.txt` resume files are supported.
- A resume must contain non-empty text.
- API usage may incur OpenAI charges.
- The model can only extract information present in the resume text and may return `Not Available` for missing fields.

## License

See [LICENSE](LICENSE) for license information.
