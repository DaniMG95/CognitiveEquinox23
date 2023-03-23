import numpy as np
from nltk.corpus import stopwords as nltk_stopwords
import tensorflow_hub as hub
import tensorflow_text
import tensorflow as tf


MODEL_URL = 'https://tfhub.dev/google/universal-sentence-encoder-multilingual/3'


class DataToVector:
    __model_embed = None
    __stopwords = None
    __device = "/gpu:0"

    def __new__(cls):
        if cls.__model_embed is None:
            model_url = MODEL_URL
            cls.__model_embed = hub.load(model_url)
        cls.__stopwords = set(nltk_stopwords.words('english'))

        cls.__device = "/gpu:0" if tf.config.list_physical_devices('GPU') else 'CPU'

        return super().__new__(cls)

    def prepare_input(self, input_string: str) -> np.ndarray:
        normalized_input_string = ' '.join(
            word for word in input_string.split() if word not in self.__stopwords
        ).strip(' ')
        # Get the embeddings of input
        with tf.device(self.__device):
            emb_question = self.__model_embed(normalized_input_string).numpy()
        return emb_question