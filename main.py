from conversation_logger import ConversationLogger
from conversation_generator import ConversationGenerator
from config import MODEL_NAME, TURNS_PER_AGENT, LOG_FILE_NAME
    
if __name__ == "__main__":
    conversation_generator = ConversationGenerator(MODEL_NAME, TURNS_PER_AGENT)
    conversation_generator.initiate_conversation()
    conversation_logger = ConversationLogger(LOG_FILE_NAME, conversation_generator.generate_conversation_history())
    conversation_logger.write_log_file()