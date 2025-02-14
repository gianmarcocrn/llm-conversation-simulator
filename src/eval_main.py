import argparse, os

from llm_judge_evaluator import run_evaluation
from config import PERSONAS_LOG_DIR_NAME

parser = argparse.ArgumentParser(description="Run a conversational data evaluator with a specified LLM")
parser.add_argument("model_identifier", type=str, help="The LMStudio identifier of the LLM model to use.")
parser.add_argument("conversation_file_name", type=str, help="The file path to load the conversation log from.")
parser.add_argument("persona_file_name", type=str, help="The file path to load the persona setting from.")
args = parser.parse_args()

if __name__ == "__main__":
    with open(os.path.join(PERSONAS_LOG_DIR_NAME, args.persona_file_name), "r", encoding="utf-8") as file:
        persona_setting_text = file.read()
    print("Running LLM-as-a-judge Evaluation...")
    run_evaluation(args.model_identifier, args.conversation_file_name, persona_setting_text)