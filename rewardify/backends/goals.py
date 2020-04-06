import datetime
from typing import List, Dict
from collections import defaultdict

from rewardify.env import EnvironmentConfig

from rewardify.backends.base import AbstractBackend, CheckConfigMixin

# PLANNING
# So what this new backend is essentially supposed to do is to monitor a folder and the files in there. Each file will
# represent one goal and using the contents of these files a description, the amount of gold and the completion time
# can be set for this goal.
# But I think the idea with using folders is rather bad. In a sense that it might be working for a single person and
# with using the CLI, but in the future I might be moving the information on the goals into a database. This means
# that with my design of this module I will have to try to make it rather agnostic of how the goals are represented
# persistently...
# The "Goal" object will be the object, which is the datatype representation of a goal

class Goal:

    def __init__(self,
                 name: str,
                 description: str,
                 gold: int,
                 perpetual: bool,
                 deadline: datetime.datetime,
                 completed: List[datetime.datetime]):
        self.name = name
        self.description = description
        self.gold = gold
        self.perpetual = perpetual
        self.deadline = deadline,
        self.completed = completed


class GoalFolderBackend(CheckConfigMixin, AbstractBackend):

    EXPECTED_CONFIG = [
        'GOAL_BACKEND_FOLDER_PATH'
    ]

    def __init__(self, config: EnvironmentConfig):
        self.config = config

    # IMPLEMENTING INTERFACE
    # ----------------------

    def get_update(self) -> Dict[str, List]:
        return self.backend.get_update()

    # IMPLEMENTING MIXIN REQUIREMENTS
    # -------------------------------

    def get_config(self):
        return self.config

    def expected_config(self):
        return self.EXPECTED_CONFIG


def raise_mode_not_supported():
    raise ModuleNotFoundError("An unsupported mode has been set for the GOAL_BACKEND_MODE variable!")


class GoalBackend(CheckConfigMixin, AbstractBackend):

    EXPECTED_CONFIG = [
        'GOAL_BACKEND_MODE',
    ]

    MODE_BACKEND_MAP = defaultdict(raise_mode_not_supported, {
        'folder': GoalFolderBackend
    })

    def __init__(self):
        self.config: EnvironmentConfig = EnvironmentConfig.instance()
        # The "check_config" method will check if the variables names from the method "expected_config" are represented
        # in the config object, which is returned by "get_config". This functionality is implemented by the
        # CheckConfigMixin.
        # After this method has run without any exceptions, we can assume, that the config contains all the variables
        # which we need
        self.check_config()

        self.mode = self.config.GOAL_BACKEND_MODE
        self.backend = self.MODE_BACKEND_MAP[self.mode]()

    # IMPLEMENTING INTERFACE
    # ----------------------

    def get_update(self) -> Dict[str, List]:
        return self.backend.get_update()

    # IMPLEMENTING MIXIN REQUIREMENTS
    # -------------------------------

    def get_config(self):
        return self.config

    def expected_config(self):
        return self.EXPECTED_CONFIG

