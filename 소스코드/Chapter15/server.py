from concurrent import futures
import grpc
import time
from grpc_health.v1 import health_pb2, health_pb2_grpc
from grpc_health.v1.health import HealthServicer
from grpc_health.v1.health_pb2 import HealthCheckResponse

class HealthCheck(HealthServicer):
    def __init__(self):
        # 서비스 상태를 저장하는 딕셔너리
        self.status_map = {
            "": HealthCheckResponse.SERVING,
            "my_service": HealthCheckResponse.SERVING,
        }

    def Check(self, request, context):
        # 요청된 서비스의 상태를 확인하여 응답
        status = self.status_map.get(request.service, HealthCheckResponse.SERVICE_UNKNOWN)
        return health_pb2.HealthCheckResponse(status=status)

    def Watch(self, request, context):
        # 상태 변화를 스트리밍으로 전송 (예제에서는 단순 응답)
        while True:
            status = self.status_map.get(request.service, HealthCheckResponse.SERVICE_UNKNOWN)
            yield health_pb2.HealthCheckResponse(status=status)
            time.sleep(5)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServicer_to_server(HealthCheck(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()