
import grpc
import chat_pb2
import chat_pb2_grpc
import asyncio

async def receive_messages(stub, user_name):
    async for message in stub.ReceiveMessages(chat_pb2.User(name=user_name)):
        print(f"{message.sender}: {message.content}")

async def send_messages(stub, user_name, receiver_name):
    while True:
        message_content = await asyncio.get_event_loop().run_in_executor(None, input, )
        await stub.SendMessage(chat_pb2.Message(sender=user_name, receiver=receiver_name, content= '\n received:' + message_content + '\n'))

async def main():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        
        user_name = input("Enter your name: ")
        response = await stub.ConnectUser(chat_pb2.User(name=user_name))
        if not response.success:
            print(response.message)
            return
        
        receiver_name = input("Enter receiver name: ")
        
        await asyncio.gather(
            receive_messages(stub, user_name),
            send_messages(stub, user_name, receiver_name)
        )

if __name__ == '__main__':
    asyncio.run(main())