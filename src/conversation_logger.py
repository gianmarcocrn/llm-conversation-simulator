import os
from datetime import datetime

class ConversationLogger:
    def __init__(self, file_name, conversation_history):
        self.file_name = file_name
        self.conversation_history = conversation_history
    
    def write_log_file(self):
        current_datetime_string = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        file_path = os.path.join("logs", f"{self.file_name}_{current_datetime_string}.txt")
        os.makedirs("logs", exist_ok=True)
        file = open(file_path, "w")
        for i in self.conversation_history:
            file.write(i['name'] + ": \n" + i['content'] + "\n\n-----------------------------------------------------------------------------------------------------------------------\n\n")
        file.close()