import sys
from utils import MarkovDB

if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit('USAGE: python3 main.py <input-file.txt>')

    db = MarkovDB(sys.argv[1])

    # Allow user to query DB
    while(True):
        word = input("\nPlease enter a keyword: ")
        db.query(word)
