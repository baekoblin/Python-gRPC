import grpc
from concurrent import futures
import interceptor_example_pb2
import interceptor_example_pb2_grpc

# 로깅 인터셉터
class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        print(f"Received request for method: {method}")
        response = continuation(handler_call_details)
        print(f"Sending response for method: {method}")
        return response

# EchoService 서비스 구현
class EchoServiceServicer(interceptor_example_pb2_grpc.EchoServiceServicer):
    def Echo(self, request, context):
        return interceptor_example_pb2.EchoResponse(message=request.message)

def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[LoggingInterceptor()]
    )
    interceptor_example_pb2_grpc.add_EchoServiceServicer_to_server(EchoServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()