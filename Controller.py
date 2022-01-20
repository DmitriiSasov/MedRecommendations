import os

from create_pdf import DocGenerator
from threading import Timer


class RecommendationController:

    doc_generator = DocGenerator()

    # Удаляем файл
    # path - строка - путь к файлу, который надо удалить
    def __remove_file(self, path):  # path
        os.remove(path)

    def generate_recommendation(self, nozology_names: list):
        doc_name = self.doc_generator.make_pdf(nozology_names)

        if doc_name is False:
            return False

        url = 'static/' + doc_name
        timer = Timer(600, self.__remove_file, args=['static/' + doc_name])
        timer.start()

        return url
