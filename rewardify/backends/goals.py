from typing import List, Dict

from rewardify.backends.base import AbstractBackend, CheckConfigMixin

# PLANNING
# So what this new backend is essentially supposed to do is to monitor a folder and the files in there. Each file will
# represent one goal and using the contents of these files a description, the amount of gold and the completion time
# can be set for this goal.
# But I think the idea with using folders is rather bad. In a sense that it might be working for a single person and
# with using the CLI, but in the future I might be moving the information on the goals into a database. This means
# that with my design of this module I will have to try to make it rather agnostic of how the goals are represented
# persistently...


class Goal:

    def __init__(self):
        pass


class GoalFolderBackend(CheckConfigMixin, AbstractBackend):

    def get_update(self) -> Dict[str, List]:
        pass
