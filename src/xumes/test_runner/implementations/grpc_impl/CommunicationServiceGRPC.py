import grpc
import xumes_pb2
import xumes_pb2_grpc

from xumes.test_runner.i_communication_service import ICommunicationService


class CommunicationServiceGRPC(ICommunicationService):

    def __init__(self, host: str):
        self.host = host
        self.channel = grpc.insecure_channel(f"{host}:50051")  # Mettez le bon port ici
        self.stub = xumes_pb2_grpc.GameServiceStub(self.channel)

    def start_scenario(self, name: str) -> int:
        request = xumes_pb2.Request(command="start_scenario", name=name)
        response = self.stub.StartScenario(request)
        return response.port
