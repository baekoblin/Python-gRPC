import grpc
from concurrent import futures
import chat_pb2
import chat_pb2_grpc

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.connected_users = {}

    def ChatStream(self, request_iterator, context):
        user_name = None
        for message in request_iterator:
            if user_name is None:
                user_name = message.sender
                self.connected_users[user_name] = context 

            receiver = message.receiver
            if receiver in self.connected_users:
                # 수정된 부분: yield를 사용하여 메시지 전송
                yield chat_pb2.Message(
                    sender=user_name,
                    receiver=receiver,
                    content=message.content
                ) 

            yield message 
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50051')  # 포트 설정
    server.start()
    print("서버가 50051 포트에서 시작되었습니다.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
