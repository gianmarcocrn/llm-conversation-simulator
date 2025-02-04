import argparse

from conversation_logger import ConversationLogger
from conversation_generator import ConversationGenerator
from llm_judge_evaluator import run_evaluation
from config import TURNS_PER_AGENT, LOG_FILE_NAME, IS_AUTOMATIC_PERSONA_GENERATION, RUN_EVALUATION, PRIMARY_PERSONA_CHARACTERISTICS, SECONDARY_PERSONA_CHARACTERISTICS

parser = argparse.ArgumentParser(description="Run a conversational data simulator with a specified LLM")
parser.add_argument("model_identifier", type=str, help="The LMStudio identifier of the LLM model to use.")
args = parser.parse_args()

if __name__ == "__main__":
    conversation_generator = ConversationGenerator(args.model_identifier, TURNS_PER_AGENT, IS_AUTOMATIC_PERSONA_GENERATION)
    conversation_generator.initiate_conversation()
    conversation_logger = ConversationLogger(LOG_FILE_NAME, conversation_generator.generate_conversation_history())
    conversation_log_filename = conversation_logger.write_and_return_log_file()
    if (RUN_EVALUATION):
        print("Running LLM-as-a-judge Evaluation...")
        run_evaluation(args.model_identifier, conversation_log_filename, conversation_generator.get_first_persona_setting())