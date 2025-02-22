import os
from datetime import datetime

from config import CONVERSATION_LOG_DIR_NAME

class ConversationLogger:
    def __init__(self, file_name, conversation_history):
        self.file_name = file_name
        self.conversation_history = conversation_history
    
    def write_and_return_log_file(self):
        current_datetime_string = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        dynamic_file_name = f"{self.file_name}_{current_datetime_string}.txt"
        file_path = os.path.join(CONVERSATION_LOG_DIR_NAME, dynamic_file_name)
        os.makedirs(CONVERSATION_LOG_DIR_NAME, exist_ok=True)
        file = open(file_path, "w")
        conversation_turn_count = 0
        for index,turn in enumerate(self.conversation_history):
            if (turn['name'] == 'user proxy'):
                if (index == 0):
                    file.write("Conversation topic prompt: " + "'" + turn['content'] + "'" + "\n\n-------------------------------------------------------------------------------------------------------------------------------------\n\n")
                continue
            conversation_turn_count += 1
            file.write(turn['name'] + " - Conversation turn " + str(conversation_turn_count) + ": \n" + "'" + turn['content']+ "'" + "\n\n-------------------------------------------------------------------------------------------------------------------------------------\n\n")
        file.close()
        return dynamic_file_name