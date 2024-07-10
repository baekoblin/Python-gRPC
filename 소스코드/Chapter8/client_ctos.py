import grpc
import streaming_pb2
import streaming_pb2_grpc

def generate_requests():
    # 클라이언트에서 보낼 데이터를 생성하는 부분
    messages = ["message 3", "message 2", "message 3"]
    for msg in messages:
        # 각 메시지를 RequestMessage로 변환하여 스트리밍
        yield streaming_pb2.RequestMessage(data=msg)

def run():
    # 서버와의 연결 설정
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = streaming_pb2_grpc.StreamingServiceStub(channel)
        # 서버에 스트리밍 데이터를 보내고 응답 받기
        response = stub.StreamData(generate_requests())
        # 서버의 응답 출력
        print("Response from server: " + response.result)

if __name__ == '__main__':
    run()