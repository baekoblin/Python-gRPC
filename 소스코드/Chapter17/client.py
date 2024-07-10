import grpc
import wait_example_pb2
import wait_example_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = wait_example_pb2_grpc.EchoServiceStub(channel)
        
        try:
            response = stub.Echo(wait_example_pb2.EchoRequest(message="Hello, gRPC!"), timeout=1)
            print(f"Response: {response.message}")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run()