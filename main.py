# print("TOP OF FILE")
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.config_loader import load_config


def main():
    try:
        # Load configuration file
        config = load_config(config_path="config/config.yaml")

        # Load environment variable
        load_dotenv()
        api_key = os.getenv(f"{config['llm']['api_key']}")

        client = OpenAI(api_key=api_key)

        config["client"] = client

        # Import processor and load config
        from src.processor import Processor

        # start pipeline
        Processor(config=config)
    except Exception as e:
        print(f"Pipeline Failed: {e}")


if __name__ == "__main__":
    main()
