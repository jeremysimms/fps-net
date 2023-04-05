from fastcore.all import *
from fastai.vision.all import *
from fastcore.utils import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("src", help="Path to the images folder")
parser.add_argument("dest", help="Where to save the resized versions")
parser.add_argument("--max_size", default=224, help="The width of the output images.")
args = parser.parse_args()

resize_images(args.src, dest=args.dest, max_size=args.max_size, recurse=True)