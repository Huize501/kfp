import os

import tensorflow as tf
from tensorflow import gfile

def write_to_file(object_to_dump, output_path):

  with tf.io.gfile.GFile(output_path, "w") as file:
    file.write(object_to_dump)

