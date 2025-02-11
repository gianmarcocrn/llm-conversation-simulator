import argparse, random

from conversation_logger import ConversationLogger
from conversation_generator import ConversationGenerator
from llm_judge_evaluator import run_evaluation
from utils import save_text_to_file_with_unique_name
from config import FIXED_TURNS_PER_AGENT, CONVERSATION_LOG_FILE_NAME, IS_AUTOMATIC_PERSONA_GENERATION, RUN_EVALUATION_ON_SAME_MODEL_AS_GENERATION, IS_RANDOM_CONVERSATION_TOPIC, IS_VARIABLE_NUMBER_OF_TURNS, MINIMUM_TURNS_PER_AGENT, MAXIMUM_TURNS_PER_AGENT

parser = argparse.ArgumentParser(description="Run a conversational data simulator with a specified LLM")
parser.add_argument("model_identifier", type=str, help="The LMStudio identifier of the LLM model to use.")
args = parser.parse_args()

if __name__ == "__main__":
    if (IS_VARIABLE_NUMBER_OF_TURNS):
        turns_per_agent = random.randint(MINIMUM_TURNS_PER_AGENT, MAXIMUM_TURNS_PER_AGENT)
    else:
        turns_per_agent = FIXED_TURNS_PER_AGENT
    conversation_generator = ConversationGenerator(args.model_identifier, turns_per_agent, IS_AUTOMATIC_PERSONA_GENERATION, IS_RANDOM_CONVERSATION_TOPIC)
    conversation_generator.initiate_conversation()
    conversation_logger = ConversationLogger(CONVERSATION_LOG_FILE_NAME, conversation_generator.generate_conversation_history())
    conversation_log_filename = conversation_logger.write_and_return_log_file()
    if (RUN_EVALUATION_ON_SAME_MODEL_AS_GENERATION):
        print("Running LLM-as-a-judge Evaluation...")
        run_evaluation(args.model_identifier, conversation_log_filename, conversation_generator.get_first_persona_setting())
        run_evaluation(args.model_identifier, conversation_log_filename, conversation_generator.get_second_persona_setting())
    else:
        save_text_to_file_with_unique_name(conversation_generator.get_first_persona_setting(), "persona_1", "personas")
        save_text_to_file_with_unique_name(conversation_generator.get_second_persona_setting(), "persona_2", "personas")
        