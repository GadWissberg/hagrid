import errno
import fcntl
import time


class FileAPI:
    # TODO check if message is in bytes or normal string (linux machine needed)

    @staticmethod
    def write_msg_into_history_file(message, chat_history_file_name):
        """
        fcntl library is used for file locking while writing to the file.
        """
        file = open(chat_history_file_name, 'a')
        try:
            fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError as e:
            if e.errno != errno.EAGAIN:
                raise
            else:
                time.sleep(0.3)
                FileAPI.write_msg_into_history_file(message, chat_history_file_name)

        file.write(message + '\n')
        fcntl.flock(file, fcntl.LOCK_UN)
        file.close()

    @staticmethod
    def get_client_history(chat_history_file_name):
        file = open(chat_history_file_name, 'r')
        file_content = file.read()
        file.close()
        return file_content
