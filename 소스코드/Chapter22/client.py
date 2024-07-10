import grpc
import auth_pb2
import auth_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        
        response = stub.GenerateToken(auth_pb2.AuthRequest(username="user", password="password"))
        print("Generated Token: ", response.token)
        
        token_response = stub.VerifyToken(auth_pb2.TokenRequest(token=response.token))
        print("Token valid: ", token_response.valid)

if __name__ == '__main__':
    run()