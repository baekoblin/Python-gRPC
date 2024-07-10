

import grpc
from concurrent import futures
import time
import chat_pb2
import chat_pb2_grpc

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.users = {}
        self.chats = {}

    def ConnectUser(self, request, context):
        if request.name in self.users:
            return chat_pb2.ConnectionStatus(success=False, message="User already connected")
        self.users[request.name] = context
        self.chats[request.name] = []
        return chat_pb2.ConnectionStatus(success=True, message="User connected")

    def SendMessage(self, request, context):
        if request.receiver not in self.users:
            return chat_pb2.Empty()
        self.chats[request.receiver].append(request)
        return chat_pb2.Empty()

    def ReceiveMessages(self, request, context):
        while True:
            if request.name in self.chats and self.chats[request.name]:
                message = self.chats[request.name].pop(0)
                yield message
            time.sleep(0.1)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()