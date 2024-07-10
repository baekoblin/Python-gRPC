from concurrent import futures
import grpc
from grpc_reflection.v1alpha import reflection
import reflection_example_pb2
import reflection_example_pb2_grpc

class EchoServiceServicer(reflection_example_pb2_grpc.EchoServiceServicer):
    def Echo(self, request, context):
        return reflection_example_pb2.EchoResponse(message=request.message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reflection_example_pb2_grpc.add_EchoServiceServicer_to_server(EchoServiceServicer(), server)
    
    # Reflection 서비스 등록
    SERVICE_NAMES = (
        reflection_example_pb2.DESCRIPTOR.services_by_name['EchoService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()