from typing import Dict, List
from collections import defaultdict

from rewardify.backends.base import AbstractBackend


def combine_backends(*backend_classes):
    """

    CHANGELOG

    Added 06.04.2020

    :param backend_classes:
    :return:
    """

    def get_string():
        """

        CHANGELOG

        Added 06.04.2020

        :return:
        """
        template = "Combination of Backends: {}"
        backend_strings = [str(backend_class) for backend_class in backend_classes]
        _string = ', '.join(backend_strings)
        return template.format(_string)

    def get_length():
        """
        CHANGELOG

        Added 06.04.2020
        :return:
        """
        return len(backend_classes)

    class CombinationMetaClass(type):
        """
        CHANGELOG

        Added 06.04.2020
        """

        def __len__(self):
            return get_length()

        def __str__(self):
            return get_string()

    class Combination(AbstractBackend, metaclass=CombinationMetaClass):
        """

        CHANGELOG

        Added 06.04.2020

        """

        # INSTANCE METHODS
        # ----------------

        def __init__(self):
            """
            The constructor

            CHANGELOG

            Added 06.04.2020
            """
            self.backends = []
            for backend_class in backend_classes:
                backend_object = backend_class()
                self.backends.append(backend_object)

        def get_update(self) -> Dict[str, List]:
            """
            CHANGELOG

            Added 06.04.2020

            :return:
            """
            combined_dict = defaultdict(list)
            for backend in self.backends:
                _dict = backend.get_update()
                combined_dict = self._insert_update_dict(combined_dict, _dict)
            return combined_dict

        # MAGIC METHODS
        # -------------

        def __len__(self):
            return get_length()

        def __str__(self):
            return get_string()

        # STATIC METHODS
        # --------------

        @classmethod
        def _insert_update_dict(cls, combined_dict: defaultdict, update_dict: Dict[str, List]) -> defaultdict:
            """
            CHANGELOG

            Added 06.04.2020

            :param combined_dict:
            :param update_dict:
            :return:
            """
            for key, value in update_dict.items():
                combined_dict[key] += value

            return combined_dict

    return Combination
