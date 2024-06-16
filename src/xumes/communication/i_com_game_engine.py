from typing import List, Dict


class IComGameEngine:

    def start_scenario(self, name: str, methods: List[Dict], fps_limit: int, render: bool):
        raise NotImplementedError

    def stop_scenario(self, port: int):
        raise NotImplementedError

    def start_scenarios(self, name: str, methods: List[Dict], fps_limit: int, render: bool):
        raise NotImplementedError

    def stop_scenarios(self, pids: List[int]):
        raise NotImplementedError
