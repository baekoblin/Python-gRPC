from concurrent import futures
import grpc
import metadata_example_pb2
import metadata_example_pb2_grpc

class EchoServiceServicer(metadata_example_pb2_grpc.EchoServiceServicer):
    def Echo(self, request, context):
        # 요청 Metadata 읽기
        metadata = dict(context.invocation_metadata())
        print("Received metadata from client:", metadata)

        # 응답 Metadata 설정
        context.set_trailing_metadata((('server-metadata-key', 'server-metadata-value'),))
        
        return metadata_example_pb2.EchoResponse(message=request.message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    metadata_example_pb2_grpc.add_EchoServiceServicer_to_server(EchoServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()