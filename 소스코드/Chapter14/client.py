import grpc
import error_handling_example_pb2
import error_handling_example_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = error_handling_example_pb2_grpc.CalculatorStub(channel)
        
        # 유효한 요청
        try:
            response = stub.Divide(error_handling_example_pb2.DivideRequest(dividend=10, divisor=2))
            print(f"Quotient: {response.quotient}")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")
        
        # 잘못된 요청: 분모가 0인 경우
        try:
            response = stub.Divide(error_handling_example_pb2.DivideRequest(dividend=10, divisor=0))
            print(f"Quotient: {response.quotient}")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run()