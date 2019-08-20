import logging
import os
import sys

import argparse
import utils
import time
import os
from pathlib import Path

def get_args():
    
    parser = argparse.ArgumentParser(
        description="ArgeParser"
        )

    parser.add_argument('--output-path-file', 
                        help="Path to where you write file that has the URI pathoutput",
                        required=True,
                        type=str,
                        default=1
                        )


    parser.add_argument('--name', 
                        help="Your name as a string",
                        required=True,
                        type=str,
                        default=1
                        )

    arguments = parser.parse_args()

    return arguments

def main():

    args = get_args()

    print(args.output_path_file)
    print(args.name)

    Path(args.output_path_file).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_path_file).write_text(args.name)

if __name__ == '__main__':
    main()

    
