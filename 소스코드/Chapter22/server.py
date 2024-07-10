import grpc
from concurrent import futures
import auth_pb2
import auth_pb2_grpc
import jwt
import datetime

SECRET_KEY = "your_secret_key"

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def GenerateToken(self, request, context):
        if request.username == "user" and request.password == "password":
            payload = {
                "username": request.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return auth_pb2.AuthResponse(token=token)
        else:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid credentials")
    
    def VerifyToken(self, request, context):
        try:
            jwt.decode(request.token, SECRET_KEY, algorithms=["HS256"])
            return auth_pb2.TokenResponse(valid=True)
        except jwt.ExpiredSignatureError:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token expired")
        except jwt.InvalidTokenError:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()