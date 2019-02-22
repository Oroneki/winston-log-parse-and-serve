import argparse
import os

parser = argparse.ArgumentParser(description='Parse and Serve Winston Logs.')
parser.add_argument('-database-path', '--db', type=str,
                    help='database-path', default=os.environ.get('DATABASE_PATH'))
parser.add_argument('-logs-folder', '--f', '-logs', type=str,
                    help='database-path', default=os.environ.get('LOGS_FOLDER_PATH'))


args = parser.parse_args()


if __name__ == "__main__":
    print(args)
