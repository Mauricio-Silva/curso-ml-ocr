from deep_translator import GoogleTranslator, single_detection
from werkzeug.exceptions import InternalServerError
from keras.src.engine.sequential import Sequential
from common import API_KEY, MODEL_PATH, Filenames
from numpy import frombuffer, uint8, array, ones
from werkzeug.datastructures import FileStorage
from pytesseract import image_to_data, Output
from keras.models import load_model
from traceback import print_exc
from pandas import DataFrame
from flask import abort
from os import mkdir
from cv2 import (
    COLOR_BGR2GRAY,
    THRESH_BINARY,
    IMREAD_COLOR,
    INTER_AREA,
    MORPH_OPEN,
    morphologyEx,
    threshold,
    imdecode,
    cvtColor,
    imwrite,
    resize
)
# cSpell:ignoreRegExp string


class GetFilmOpinion:
    MODEL: Sequential = None
    THRESHOLD = 25
    GOOD_MOVIE = "O Filme é Bom!"
    BAD_MOVIE = "O Filme é Ruim!"

    def __init__(self):
        self.api_key = bytes.fromhex(API_KEY).decode("utf-8")
        print(self.api_key)

    @classmethod
    def load_ml_model(cls):
        print("\033[33mLoading ML Model...\033[m", end="\r")
        model = load_model(MODEL_PATH)
        if not model:
            raise RuntimeError("\n\033[31mError in Loading Model\033[m")
        cls.MODEL: Sequential = model
        print("\033[33mLoading ML Model...\033[m\u2705")

    def handle(self, buffer_file: FileStorage):
        self.__filenames = Filenames(buffer_file.filename)
        try:
            self.__handle_image(buffer_file.stream.read())
        except Exception:
            print_exc()
            abort(500, "Erro ao Processar a Imagem")
        try:
            self.__handle_text()
        except InternalServerError as error:
            raise error
        except Exception:
            print_exc()
            abort(500, "Erro ao Processar o Texto")
        try:
            return self.__handle_classifier()
        except InternalServerError as error:
            raise error
        except Exception:
            print_exc()
            abort(500, "Erro ao Classificar o Texto")

    def __handle_image(self, file: bytes):
        bytes_array = frombuffer(file, uint8)
        image = imdecode(bytes_array, IMREAD_COLOR)

        mkdir(self.__filenames.folder_path)
        imwrite(self.__filenames.original_path, image)

        height, width, _ = image.shape
        scale_percent = 720 / min(height, width)

        height = int(height * scale_percent)
        width = int(width * scale_percent)
        dim = (width, height)

        image = resize(image, dim, interpolation=INTER_AREA)
        gray_image = cvtColor(image, COLOR_BGR2GRAY)

        kernel = ones((3, 3), uint8)
        opening_image = morphologyEx(gray_image, MORPH_OPEN, kernel)

        self.__image = threshold(opening_image, 100, 255, THRESH_BINARY)[1]
        imwrite(self.__filenames.processed_path, self.__image)

    def __handle_text(self):
        dataframe: DataFrame = image_to_data(self.__image, output_type=Output.DATAFRAME)
        dataframe.to_csv(self.__filenames.csv_path, mode="a", index=False, header=True)

        dataframe = dataframe[["conf", "text"]].query(f"conf >= {self.THRESHOLD}")
        if dataframe["text"].empty:
            abort(500, "Nenhum texto valido Encontrado")

        text = dataframe["text"].str.cat(sep=" ")
        text = text.strip().replace(r"\n", "").replace(r"\s{2,}", "")

        with open(self.__filenames.text_path, "w") as file:
            file.write(text)

        if not len(text):
            abort(500, "Texto não Encontrado")

        if single_detection(text, self.api_key) != "en":
            try:
                translator = GoogleTranslator(source="auto", target="en")
                text = translator.translate(text)
            except Exception:
                abort(500, "Erro ao Traduzir o Texto")

        self.__text = text

    def __handle_classifier(self):
        try:
            prediction = self.MODEL.predict(array([self.__text]))
        except Exception:
            abort(500, "Erro na Classificação do Texto")

        if prediction < 0:
            return self.BAD_MOVIE
        else:
            return self.GOOD_MOVIE
