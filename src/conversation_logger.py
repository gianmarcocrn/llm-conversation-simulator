import os


class ConversationLogger:
    def __init__(self, file_name, conversation_history):
        self.file_name = file_name
        self.conversation_history = conversation_history
    
    def write_log_file(self):
        file_path = os.path.join("logs", self.file_name)
        os.makedirs("logs", exist_ok=True)
        file = open(file_path, "w")
        for i in self.conversation_history:
            file.write(i['name'] + ": \n" + i['content'] + "\n\n-----------------------------------------------------------------------------------------------------------------------\n\n")
        file.close()