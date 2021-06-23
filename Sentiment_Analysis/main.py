from Sentiment_Analysis import Sentiment_Analysis
from huggingface_fine_tuner import huggingface_fine_tuner

def run_pipeline(model_name="Alkholi",text=""):
    c=Sentiment_Analysis(model_name)
    c.predict(text)
#========================================fine tuning=========================
fine_tuner=huggingface_fine_tuner(model_checkpoint="the model checkpoint name or path", training_path="training csv path",validation_path="validation csv path")
fine_tuner.train()
fine_tuner.inference("text to be inferred")

    