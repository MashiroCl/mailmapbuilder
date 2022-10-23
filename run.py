import argparse
import os.path
from core.repository import Repository
from core.main import MailMap

def command_line():
    parser = argparse.ArgumentParser(description="Automatically build .mailmap")
    parser.add_argument('-i', '--input', help = "path for repository need to be built .mailmap")
    parser.add_argument('-o', '--output', help = "output path for .mailmap file")

    return parser.parse_args()


if __name__ =="__main__":
    args = command_line()
    MailMap(Repository(args.input)).build_mailmap(os.path.join(args.output, ".mailmap"))