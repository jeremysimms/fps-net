#!/usr/bin/env python
import argparse
import json
from fastcore.all import *
from fastai.vision.all import *
from fastcore.utils import *

parser = argparse.ArgumentParser()
parser.add_argument("model", default="val-detector.pkl", help="Path to the model")
parser.add_argument("files", help="Path to the image file.")
args = parser.parse_args()
learn = load_learner(args.model, cpu=True)
test_dl = learn.dls.test_dl(get_image_files(args.files), with_labels=True, shuffle=True)
validation = learn.validate(dl=test_dl)
preds = learn.get_preds(dl=test_dl, with_decoded=True)
print(accuracy(preds[0], preds[1]))

exit(0)