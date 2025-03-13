import argparse, os

from llm_judge_evaluator import run_evaluation_from_file_names
from config import PERSONAS_LOG_DIR_NAME

parser = argparse.ArgumentParser(description="Run a conversational data evaluator with a specified LLM")
parser.add_argument("model_identifier", type=str, help="The LMStudio identifier of the LLM model to use.")
parser.add_argument("conversation_file_name", type=str, help="The file path to load the conversation log from.")
parser.add_argument("persona_file_name", type=str, help="The file path to load the persona setting from.")
args = parser.parse_args()

if __name__ == "__main__":
    print("Running LLM-as-a-judge Evaluation...")
    run_evaluation_from_file_names(args.model_identifier, args.conversation_file_name, args.persona_file_name)