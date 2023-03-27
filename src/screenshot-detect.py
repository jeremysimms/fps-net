#!/usr/bin/env python
import argparse
import json
from fastcore.all import *
from fastai.vision.all import *
from fastcore.utils import *

parser = argparse.ArgumentParser()
parser.add_argument("model", default="val-detector.pkl", help="Path to the model")
parser.add_argument("file", help="Path to the image file.")
args = parser.parse_args()
learn = load_learner(args.model, cpu=True)

def classify_image(file):
    img = PILImage.create(file)
    img.load()
    img = img.convert("RGB")
    with learn.no_bar():
        label,_,probs = learn.predict(img)
        return (label, dict(zip(learn.dls.vocab, map(float, probs))))

(label, results) = classify_image(args.file)
print(json.dumps( results ))
exit(0)