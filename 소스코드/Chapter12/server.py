import grpc
from concurrent import futures
import example_pb2
import example_pb2_grpc

class DataServiceServicer(example_pb2_grpc.DataServiceServicer):
    def GetData(self, request, context):
        data_id = request.data_id
        # 데이터 가져오기 (예: 데이터베이스에서 조회)
        data = b"This is a large data example. " * 10000  # 대용량 데이터 생성
        print(context.compression())
        return example_pb2.DataResponse(data=data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                        compression=grpc.Compression.Gzip)  # Gzip 압축 사용
    example_pb2_grpc.add_DataServiceServicer_to_server(DataServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()