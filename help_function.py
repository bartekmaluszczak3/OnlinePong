import threading


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


def read_file(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    lst = []
    for line in lines:
        lst.append(line[:-1])
    return lst

def save_to_file(filename, item):
    file = open(filename, "a")
    file.write(item)
    file.write("\n")
    file.close()
