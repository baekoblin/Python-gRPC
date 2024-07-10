from concurrent import futures
import grpc
import time
from grpc_health.v1 import health_pb2, health_pb2_grpc
from grpc_health.v1.health import HealthServicer
from grpc_health.v1.health_pb2 import HealthCheckResponse

class HealthCheck(HealthServicer):
    def __init__(self):
        self.status_map = {
            "": HealthCheckResponse.SERVING,
            "my_service": HealthCheckResponse.SERVING,
        }
        self.start_time = time.time()

    def Check(self, request, context):
        current_time = time.time()
        if current_time - self.start_time > 10:  # 10초 후에 비정상 상태로 변경
            return health_pb2.HealthCheckResponse(status=HealthCheckResponse.NOT_SERVING)
        status = self.status_map.get(request.service, HealthCheckResponse.SERVICE_UNKNOWN)
        return health_pb2.HealthCheckResponse(status=status)

    def Watch(self, request, context):
        while True:
            current_time = time.time()
            if current_time - self.start_time > 10:  # 10초 후에 비정상 상태로 변경
                yield health_pb2.HealthCheckResponse(status=HealthCheckResponse.NOT_SERVING)
            else:
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
