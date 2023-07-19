import logging
from queue import Queue, Empty
from threading import Thread, Condition

from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.game_module.i_communication_service_game import ICommunicationServiceGame
from xumes.game_module.i_event_factory import EventFactory
from xumes.game_module.i_game_state_observer import IGameStateObserver
from xumes.game_module.test_runner import TestRunner
from xumes.game_module.errors import KeyNotFoundError


class GameService:
    """
    The `GameService` class is a central component of Xumes. It manages communication between communication service,
    the execution of the game itself, and external events that can modify the game state.

    Attributes:
        observer (IGameStateObserver): An object implementing the `IGameStateObserver` interface, used to observe the game state.
        test_runner (TestRunner): An object responsible for executing the test and updating the game state.
        event_factory (EventFactory): An object implementing the `IEventFactory` interface, used to create events within the game.
        communication_service (ICommunicationServiceGame): An object responsible for communication with other the training service.

    Methods:
        run_communication_service(): Starts the communication service thread.
        run_test_runner(run_func): Starts the game loop if this is the main thread. `run_func` is the game loop function to execute.
        run(): Executes the game by starting both the communication service and the game loop.
        run_render(): Similar to `run()`, but runs the game loop with rendering.
        stop(): Stops both threads currently running.
        wait(): The first method executed in the game loop. It allows the game to wait for an event sent by the training service.
        update_event(event): Method used to accept external modifications to the game, such as reset. `event` represents an external event that can modify the game state.
    """

    def __init__(self,
                 test_runner: TestRunner,
                 event_factory: EventFactory,
                 communication_service: ICommunicationServiceGame,
                 ):

        self.comm_thread = None
        self.game_update_condition = Condition()
        self.get_state_condition = Condition()
        self.tasks = Queue()
        self.observer = None

        self.test_runner = test_runner
        self.test_runner.set_client(self)

        self.event_factory = event_factory
        self.inputs = []

        self.communication_service = communication_service

        self.is_finished = False

    def run_communication_service(self):
        """
        Start the communication service thread.
        """
        self.comm_thread = Thread(target=self.communication_service.run, args=[self])
        self.comm_thread.start()

    def run(self):
        """
        - The communication service thread, used to send state and get actions.\n
        - The game on the main thread, used to make run the game loop.
        """
        self.run_communication_service()
        self.test_runner.delete_screen()
        self.test_runner.run_test()

    def run_render(self):
        """
        Same has run but for the game thread, we run with rendering.
        """
        self.run_communication_service()
        self.test_runner.run_test_render()

    def stop(self):
        """
        Stop communication thread.
        """
        logging.info("Stopping game loop...")
        self.comm_thread.join()
        self.communication_service.stop()

    def wait(self) -> bool:
        """
        First executed method in the game loop, used to make the game
        wait for an event send by the training service.

        :return: True if the game has been reset, False otherwise. We don't compute the game loop if the game has been reset.
        """

        # Notify the communication service to send the state to
        # the training service.
        with self.get_state_condition:
            self.get_state_condition.notify()

        # Clear every previous events
        self.event_factory.clear()

        # Stop every previous events
        for key_input in self.inputs:
            key_input.release()
        self.inputs.clear()

        # Wait event
        if not self.is_finished:
            with self.game_update_condition:
                self.game_update_condition.wait()

        # Run events from communication thread
        reset = False
        while not self.tasks.empty():
            try:
                task = self.tasks.get(block=False)
                func = task[0]
                args = task[1:]
                func(*args)
                if func.__name__ == "update_event" and args[0] == "reset":
                    reset = True
            except Empty:
                break

        # Run new events
        for key_input in self.inputs:
            key_input.press()
        return reset  # If reset is true, we don't need to run the game loop because we want to notify the new state.

    def add_input(self, input_str):
        try:
            key_input = self.event_factory.find_input(input_str)
            self.inputs.append(key_input)
        except KeyNotFoundError:
            logging.error(f"Key {input_str} not found in the event factory.")

    def update_event(self, event: str):
        """
        Method used to accept external modification on the game,
        like reset.
        :param event: representation of an extern event on the game like reset.
        """
        if event == "reset":
            self.test_runner.reset()
        if event == "random_reset":
            self.test_runner.random_reset()
        if event == "finished":
            self.is_finished = True
            raise RunningEndsError()
