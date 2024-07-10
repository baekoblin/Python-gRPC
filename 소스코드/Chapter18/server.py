import grpc
from concurrent import futures
import example_pb2
import example_pb2_grpc
import time

class ExampleServiceServicer(example_pb2_grpc.ExampleServiceServicer):
    def UnaryCall(self, request, context):
        # 의도적으로 50% 확률로 실패 시뮬레이션
        if time.time() % 2 < 1:
            context.abort(grpc.StatusCode.UNAVAILABLE, "Server unavailable")
        return example_pb2.ExampleResponse(message=f"Received: {request.message}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_ExampleServiceServicer_to_server(
        ExampleServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
