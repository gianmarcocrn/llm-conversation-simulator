class ConversationLogger:
    def __init__(self, file_name, conversation_history):
        self.file_name = file_name
        self.conversation_history = conversation_history
    
    def write_log_file(self):
        file = open(self.file_name, "w")
        for i in self.conversation_history:
            file.write(i['name'] + ": \n" + i['content'] + "\n\n-----------------------------------------------------------------------------------------------------------------------\n\n")
        file.close()