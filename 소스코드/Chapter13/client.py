import grpc
import interceptor_example_pb2
import interceptor_example_pb2_grpc

# 클라이언트 로깅 인터셉터
class LoggingInterceptor(grpc.UnaryUnaryClientInterceptor):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        method = client_call_details.method
        print(f"Sending request to method: {method}")
        response = continuation(client_call_details, request)
        print(f"Received response from method: {method}")
        return response

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        intercept_channel = grpc.intercept_channel(channel, LoggingInterceptor())
        stub = interceptor_example_pb2_grpc.EchoServiceStub(intercept_channel)
        
        response = stub.Echo(interceptor_example_pb2.EchoRequest(message="Hello, gRPC!"))
        print(f"Response: {response.message}")

if __name__ == '__main__':
    run()