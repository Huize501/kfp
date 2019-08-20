import logging
import os
import sys

import argparse
import time
import os


def get_args():
    
    parser = argparse.ArgumentParser(
        description="ArgeParser"
        )

    parser.add_argument('--name', 
                        help="GCS Bucket to output model.joblib",
                        required=True,
                        type=str,
                        default=1
                        )

    arguments = parser.parse_args()

    return arguments

def main():

    args = get_args()

    name = args.name

    print(name)

if __name__ == '__main__':
    main()

    
