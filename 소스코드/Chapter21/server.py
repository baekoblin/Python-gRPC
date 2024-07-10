from concurrent import futures
import grpc
import example_pb2
import example_pb2_grpc

class ExampleServiceServicer(example_pb2_grpc.ExampleServiceServicer):
    def SayHello(self, request, context):
        response = example_pb2.HelloReply()
        response.message = f"Hello, {request.name}!"
        return response

def serve():
    # SSL/TLS 인증서를 생성합니다.
    with open('server.key', 'rb') as f:
        private_key = f.read()
    with open('server.crt', 'rb') as f:
        certificate_chain = f.read()
    
    server_credentials = grpc.ssl_server_credentials(
        ((private_key, certificate_chain,),)
    )
    
    # 서버를 생성하고 보안 포트를 추가합니다.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleServiceServicer(), server)
    server.add_secure_port('[::]:50051', server_credentials)
    
    # 서버를 시작합니다.
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
