import grpc
import example_pb2
import example_pb2_grpc
import json
def run():
    # gRPC 채널 옵션 설정
    retry_policy = {
        'maxAttempts': 5,
        'initialBackoff': '0.1s',
        'maxBackoff': '1s',
        'backoffMultiplier': 2,
        'retryableStatusCodes': ["UNAVAILABLE"],  # 상태 코드 이름 문자열로 변경
    }
    
    channel_options = [
        ("grpc.enable_retries", 1),
        ("grpc.service_config", json.dumps({'methodConfig': [{'name': [{}], 'retryPolicy': retry_policy}]}))
    ]

    channel = grpc.insecure_channel("localhost:50051", options=channel_options)
    stub = example_pb2_grpc.ExampleServiceStub(channel)

    try:
        response = stub.UnaryCall(example_pb2.ExampleRequest(message="Hello"))
        print(f"Received: {response.message}")
    except grpc.RpcError as e:
        print(f"Error: {e.code()}: {e.details()}")

if __name__ == "__main__":
    run()
