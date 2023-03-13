import threading

import helpers

if __name__ == '__main__':
    print("Hello good sir!")

    threading.Thread(target=helpers.update_servers).start()
