class FileAPI:

    @staticmethod
    def copy_msg_to_file(message, chat_history_file_name):
        file = open(chat_history_file_name, 'a')
        # TODO check if message is in bytes or normal string (linux machine needed)
        file.write(message + '\n')
        content = file.read()
        file.close()


# TODO for debugging api file
if __name__ == '__main__':
    FileAPI.copy_msg_to_file("1_2_3.txt")
