import os
from datetime import datetime

class ConversationLogger:
    def __init__(self, file_name, conversation_history):
        self.file_name = file_name
        self.conversation_history = conversation_history
    
    def write_and_return_log_file(self):
        current_datetime_string = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        dynamic_file_name = f"{self.file_name}_{current_datetime_string}.txt"
        file_path = os.path.join("logs", dynamic_file_name)
        os.makedirs("logs", exist_ok=True)
        file = open(file_path, "w")
        for i in self.conversation_history:
            file.write(i['name'] + ": \n" + i['content'] + "\n\n-----------------------------------------------------------------------------------------------------------------------\n\n")
        file.close()
        return dynamic_file_name