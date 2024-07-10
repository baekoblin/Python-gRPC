import grpc
from concurrent import futures
import messages_pb2
import messages_pb2_grpc
import time

class ChatService(messages_pb2_grpc.ChatServiceServicer):
    def ChatStream(self, request, context):
        messages = [
            "Hi!",
            "Server Streaming Example",
            "Good Bye!"
        ]
        for message in messages:
            yield messages_pb2.ChatMessage(message=message)
            time.sleep(1)  # 메시지 간 간격 조절

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messages_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("서버 시작...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
