from typing import Dict, List
from collections import defaultdict

from rewardify.backends.base import AbstractBackend


def combine_backends(*backend_classes):
    """
    Combines the usage of all the passed backend classes

    BACKGROUND

    A "backend" for the rewardify system refers to a class, which implements a possibility of gaining more
    currency by some means. What specifically triggers this acquisition of the currency is specific to the
    individual backend class. A new backend can be implemented by simply inheriting from the
    AbstractBackend base class.

    PROBLEM

    Within the configuration file a backend can be chosen by naming its class name. Now the problem is that using
    this mechanic only one backend can be used at the same time. This is where this function comes in. it can be used
    to use multiple backends at the same time.

    What this method does is essentially dynamically constructing a new class "Combination", which also implements the
    AbstractBackend base class, but which internally manages all the backends, whose classes have been passed as the
    parameters to this function

    EXAMPLE

    ```python
    from rewardify.backends import MockBackend, ForestBackend
    from rewardify.backends.combine import combine_backends

    BACKEND = combine_backends(ForestBackend, MockBackend)
    ```

    CHANGELOG

    Added 06.04.2020

    :param backend_classes:
    :return:
    """

    def get_string():
        """
        returns the string representation for the combination class

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
        Returns the amount of backends combined within the combination class

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
        This class represents the combination of several backends

        Since this class extends the AbstractBackend base class, it is also a valid backend to be used. Only that this
        class is dynamically created based on the inputs for the function.
        In the constructor of this class all the passed backends are constructed and saved within a list. When the
        "get_update" method is called on an object of this class, it will be called on all the backends in the internal
        list and then these update dicts are combined into a single one, which is returned.

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
            Returns the update dict

            The keys of the update dict are the string user names of the users for which currency is to be added. The
            values to those keys are lists of dicts. Those dicts describe one action for which currency has been earned

            CHANGELOG

            Added 06.04.2020

            :return:
            """
            # Here we are making the combined_dict a default dict, because that way it will be easier inserting new
            # individual update dicts into it for a situation in which the update dict is for a user, which is not
            # yet represented in the combined_dict. For such a case you would usually have to define if/else cases but
            # not when you can assume that for any new key an empty list will be assumed anyways...
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
            Updates the "combined_dict" with the contents of "update_dict"

            CHANGELOG

            Added 06.04.2020

            :param combined_dict:
            :param update_dict:
            :return:
            """
            for key, value in update_dict.items():
                # combined_dict is a defaultdict with the "list" factory. Well the important thing to remember is that
                # both the values of the combined_dict and the update dict are lists, which means that the "+="
                # operator here really just merges these lists.
                # -> This is what this method is all about. Thats why we cant just use
                # combined_dict.update(update_dict), which would override the list values each time, but what we really
                # want is to merge these list values, which are one level deep into the dict.
                combined_dict[key] += value

            return combined_dict

    # The method will return the class, since in the configuration file a class has to be defined!
    return Combination
