import torch
import torch.nn.functional as torch_fun
from transformers import BertTokenizer, BertForSequenceClassification

from omdena_tools.data import DataCatalogue

_LABELS = ('positive', 'negative', 'neutral')


class SentimentAnalyzer:
    """A class for running a fine-tuned sentiment analysis model to predict
    the sentiment of given sentences.
    """

    def __init__(self, model_path):
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.labels_map = self.model.config.id2label

    @staticmethod
    def pretrained(model_name=None):
        """Load a pre-trained model provided with omdena_tools.
        Args:
            model_name (:obj:`str`, optional): Name of pre-trained model to
                load.
                Two models are available: 'arabert' and 'mbert'.
                If None, the default model ('arabert') will be loaded.
                Defaults to None.
        Returns:
            :obj:`SentimentAnalyzer`: Instance with loaded pre-trained model.
        """

        model_info = DataCatalogue.get_dataset_info('SentimentAnalysis',
                                                    model_name)
        model_path = str(model_info.path)

        return SentimentAnalyzer(model_path)

    @staticmethod
    def labels():
        """Get the list of possible sentiment labels returned by predictions.
        Returns:
            :obj:`list` of :obj:`str`: List of sentiment labels.
        """

        return list(_LABELS)

    def predict_sentence(self, sentence):
        """Predict the sentiment label of a single sentence.
        Args:
            sentence (:obj:`str`): Input sentence.
        Returns:
            :obj:`str`: The predicted sentiment label for given sentence.
        """

        # Add special tokens takes care of adding [CLS], [SEP] tokens
        input_ids = torch.tensor(
            self.tokenizer.encode(
                sentence, add_special_tokens=True,
                truncation=True, max_length=512)).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(input_ids)

        predictions = torch_fun.softmax(outputs[0].squeeze(), dim=0)
        max_prediction = torch.argmax(predictions, dim=0)
        predicted_label = self.labels_map[max_prediction.item()]

        return predicted_label

    def predict(self, sentences):
        """Predict the sentiment labels of a list of sentences.
        Args:
            sentences (:obj:`list` of :obj:`str`): Input sentences.
        Returns:
            :obj:`list` of :obj:`str`: The predicted sentiment labels for given
            sentences.
        """

        predicted_labels = []
        for i, sentence in enumerate(sentences):
            predicted_label = self.predict_sentence(sentence)
            predicted_labels.append(predicted_label)

        return predicted_labels
