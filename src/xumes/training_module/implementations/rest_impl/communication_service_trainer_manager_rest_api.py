from flask import Flask, request

from xumes.training_module.i_communication_service_trainer_manager import ICommunicationServiceTrainerManager


class CommunicationServiceTrainerManagerRestApi(ICommunicationServiceTrainerManager):
    """
    The `CommunicationServiceTrainerManagerRestApi` class implements the `ICommunicationServiceTrainerManager` interface.
    """

    def __init__(self):
        self.app = Flask(__name__)

    def connect_trainer(self, trainer_manager) -> None:
        @self.app.route("/connect", methods=['POST'])
        def connect():
            feature, scenario, port = request.json['feature'], request.json['scenario'], request.json['port']
            trainer_manager.connect_trainer(feature, scenario, port)
            return "Trainer connected!"

    def disconnect_trainer(self, trainer_manager) -> None:
        @self.app.route("/disconnect", methods=['POST'])
        def disconnect():
            feature, scenario = request.json['feature'], request.json['scenario']
            trainer_manager.disconnect_trainer(feature, scenario)
            return "Trainer disconnected!"

    def start_training(self, trainer_manager) -> None:
        @self.app.route("/start", methods=['POST'])
        def start_training():
            trainer_manager.run()
            return "Training started!"

    def reset(self, trainer_manager) -> None:
        @self.app.route("/reset", methods=['POST'])
        def reset():
            trainer_manager.reset_trainer()
            return "Training reset!"

    def ping(self):
        @self.app.route("/ping", methods=['GET'])
        def ping():
            return "pong"

    def run(self, trainer_manager, port) -> None:
        self.connect_trainer(trainer_manager)
        self.disconnect_trainer(trainer_manager)
        self.start_training(trainer_manager)
        self.reset(trainer_manager)
        self.ping()
        self.app.run(port=port)
