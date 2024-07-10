import grpc
import example_pb2
import example_pb2_grpc

def run():
    # SSL/TLS 인증서를 생성합니다.
    with open('server.crt', 'rb') as f:
        trusted_certs = f.read()
        
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    
    # 보안 채널을 생성합니다.
    channel = grpc.secure_channel('localhost:50051', credentials)
    
    # 클라이언트를 생성합니다.
    stub = example_pb2_grpc.ExampleServiceStub(channel)
    
    # 요청을 생성하고 서버에 전송합니다.
    response = stub.SayHello(example_pb2.HelloRequest(name='World'))
    print("Greeting:", response.message)

if __name__ == '__main__':
    run()
