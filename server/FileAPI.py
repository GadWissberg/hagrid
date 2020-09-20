class FileAPI:
    # TODO check if message is in bytes or normal string (linux machine needed)

    @staticmethod
    def write_msg_into_history_file(message, chat_history_file_name):
        file = open(chat_history_file_name, 'a')
        file.write(message + '\n')
        file.close()

    @staticmethod
    def get_client_history(chat_history_file_name):
        file = open(chat_history_file_name, 'r')
        file_content = file.read()
        file.close()
        return file_content
