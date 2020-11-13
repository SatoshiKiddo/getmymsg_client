import sys
from getmymsg.client import Client


__version__ = 'v1.0.2'


def main():
    sys.exit(Client().start())

