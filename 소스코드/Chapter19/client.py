import grpc
import metadata_example_pb2
import metadata_example_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = metadata_example_pb2_grpc.EchoServiceStub(channel)
        
        # 요청 시 Metadata 추가
        metadata = (('client-metadata-key', 'client-metadata-value'),)
        response, call = stub.Echo.with_call(metadata_example_pb2.EchoRequest(message="Hello, gRPC!"), metadata=metadata)
        
        print(f"Response: {response.message}")
        
        # 응답 Metadata 읽기
        server_metadata = dict(call.trailing_metadata())
        print("Received metadata from server:", server_metadata)

if __name__ == '__main__':
    run()