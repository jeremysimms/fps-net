from fastcore.all import *
from fastai.vision.all import *
import gradio as gr

learn = load_learner("../models/fps-net.pkl", cpu=True)

def classify_image(img):
    _,_,probs = learn.predict(img)
    return dict(zip(learn.dls.vocab, map(float, probs)))

image = gr.inputs.Image()
label = gr.outputs.Label()

intf = gr.Interface(fn=classify_image, inputs=image, outputs=label)
intf.launch()