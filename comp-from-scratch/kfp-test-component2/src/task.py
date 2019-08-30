import logging
import os
import sys
from tensorflow import gfile
import tensorflow as tf
import argparse


def get_args():
    
    parser = argparse.ArgumentParser(
        description="ArgeParser"
        )

    parser.add_argument('--gcspath', 
                        help="GCS Bucket where text file with name is stored",
                        required=True,
                        type=str,
                        default=1
                        )

    arguments = parser.parse_args()

    return arguments

def main():

    args = get_args()

    with tf.io.gfile.GFile(args.gcspath, "rb") as file:
      text = file.read()

    print(text)

if __name__ == '__main__':
    main()

    
