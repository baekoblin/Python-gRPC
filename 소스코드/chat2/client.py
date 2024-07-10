import grpc
import chat_pb2
import chat_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')  # 서버 주소
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    user_name = input("이름을 입력하세요: ")
    receiver_name = input("상대방 이름을 입력하세요: ")

    def generate_messages():
        while True:
            message_content = input(f"{receiver_name}에게 보낼 메시지: ")
            yield chat_pb2.Message(sender=user_name, receiver=receiver_name, content=message_content)

    # 양방향 스트림 설정
    responses = stub.ChatStream(generate_messages())
    for response in responses:
        print(f"{response.sender}: {response.content}")

if __name__ == '__main__':
    run()
