import grpc
import messages_pb2
import messages_pb2_grpc
import time

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = messages_pb2_grpc.ChatServiceStub(channel)
        
        # 메시지를 보내고 응답을 받기 위한 요청 생성기를 정의합니다.
        def request_generator():
            messages = ["Hi?", "gRPC Bidirectional!", "Well!"]
            for msg in messages:
                print(f"Client Message: {msg}")
                yield messages_pb2.ChatMessage(message=msg)
                time.sleep(2)  # 클라이언트가 다음 메시지를 준비하는데 시간 지연

        # 서버로부터 응답을 받는 스트림을 생성합니다.
        responses = stub.Chat(request_generator())

        # 서버로부터 받은 메시지를 출력합니다.
        for response in responses:
            print(f"Recieved Message: {response.message}")

if __name__ == '__main__':
    run()