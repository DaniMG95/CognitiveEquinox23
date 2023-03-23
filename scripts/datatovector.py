import numpy as np
from nltk.corpus import stopwords as nltk_stopwords
import tensorflow_hub as hub
import tensorflow_text


class DataToVector:
    __model_embed = None
    __stopwords = None

    def __new__(cls):
        if cls.__model_embed is None:
            model_url = 'https://tfhub.dev/google/universal-sentence-encoder-multilingual/3'
            cls.__model_embed = hub.load(model_url)
        cls.__stopwords = set(nltk_stopwords.words('english'))
        return super().__new__(cls)

    def prepare_input(self, input_string: str) -> np.ndarray:
        normalized_input_string = ' '.join(word for word in input_string.split()).strip(
            ' ')
        # Get the embeddings of input
        emb_question = self.__model_embed(normalized_input_string).numpy()
        return emb_question


# script = DataToVector()
# script.prepare_input(input_string='hola que tal')


