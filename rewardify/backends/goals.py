import datetime
import os
import json
from typing import List, Dict, Any

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
# Ok like, every User has to have a state associated with it, which sort of tells the system which goals have already
# be accounted for. A simple way to do this is to store a dictionary with all the dates of only those goals that are
# already accounted for. This would be efficient and easy, but thinking into the future one might want to add a
# statistics function and for that you would need a full history of ALL the goals that have been achieved... Which is
# going to be harder to implement and also less efficient...


DATE_FORMAT = "%d.%m.%Y %H:%M"


class Goal:

    def __init__(self,
                 username: str,
                 name: str,
                 description: str,
                 gold: int,
                 perpetual: bool,
                 deadline: str,
                 completed: List[str]):
        self.username = username
        self.name = name
        self.description = description
        self.gold = gold
        self.perpetual = perpetual
        self.deadline = deadline,
        self.completed = completed

    def is_completed(self):
        return len(self.completed) != 0


def default_date():
    return "01.01.1990 12:00"


class GoalBackend(CheckConfigMixin, AbstractBackend):

    EXPECTED_CONFIG = [
        'GOAL_BACKEND_FOLDER_PATH',
        'GOAL_BACKEND_STATE_PATH'
    ]

    def __init__(self):
        self.config: EnvironmentConfig = EnvironmentConfig.instance()
        # The "check_config" method will check if the variables names from the method "expected_config" are represented
        # in the config object, which is returned by "get_config". This functionality is implemented by the
        # CheckConfigMixin.
        # After this method has run without any exceptions, we can assume, that the config contains all the variables
        # which we need
        self.check_config()

        self.folder_path = self.config.GOAL_BACKEND_FOLDER_PATH
        self.state_path = self.config.GOAL_BACKEND_STATE_PATH
        self.state = self.load_state()

    # IMPLEMENTING INTERFACE
    # ----------------------

    def load_state(self) -> Dict[str, str]:
        with open(self.state_path, mode='r+') as file:
            state = defaultdict(default_date)
            _content = file.read()
            state.update(json.loads(_content))
            return state

    def save_state(self):
        with open(self.state_path, mode='r+') as file:
            file.write(json.dumps(dict(self.state)))

    def load_goals(self) -> List[Goal]:
        goals = []
        for (dirpath, dirnames, filenames) in os.walk(self.folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                _goal = self.goal_from_file(file_path)
                goals.append(_goal)
            break
        return goals

    @classmethod
    def goal_from_file(cls, path: str):
        with open(path, mode='r+') as file:
            _content = file.read()
            _dict = json.loads(_content)
            return Goal(
                _dict['username'],
                _dict['name'],
                _dict['description'],
                _dict['gold'],
                _dict['perpetual'],
                _dict['deadline'],
                _dict['completed']
            )

    def get_update(self) -> Dict[str, List]:
        update = defaultdict(list)
        goals = self.load_goals()
        for goal in goals:
            if goal.is_completed():
                _completed_date_string = goal.completed[-1]
                completed_date = datetime.datetime.strptime(_completed_date_string, DATE_FORMAT)
                _state_date_string = self.state[goal.name]
                state_date = datetime.datetime.strptime(_state_date_string, DATE_FORMAT)

                if completed_date > state_date:
                    _update = {
                        'name': goal.name,
                        'description': goal.description,
                        'gold': goal.gold,
                        'date': completed_date
                    }
                    self.state[goal.name] = completed_date.strftime(DATE_FORMAT)
                    update[goal.username].append(_update)

        self.save_state()
        return update

    # IMPLEMENTING MIXIN REQUIREMENTS
    # -------------------------------

    def get_config(self):
        return self.config

    def expected_config(self):
        return self.EXPECTED_CONFIG

