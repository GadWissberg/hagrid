class FileAPI:

    @staticmethod
    def copy_msg_to_file(chat_history_file_name):
        file = open(chat_history_file_name, 'w')


# TODO for debugging api file
if __name__ == '__main__':
    FileAPI.copy_msg_to_file("1_2_3.txt")
