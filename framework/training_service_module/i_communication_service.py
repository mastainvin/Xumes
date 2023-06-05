from typing import List


class ICommunicationService:

    def push_event(self, event) -> None:
        pass

    def push_actions(self, actions) -> None:
        pass

    def get_states(self) -> List:
        pass
