import os

def readcredentials():
    credentials = []
    
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'credentials.txt')
    
    with open (my_file, "r") as reader:    
        for line in reader:
            credentials.append(line.rstrip())
    return credentials
