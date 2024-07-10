import grpc
import example_pb2
import example_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051', compression=grpc.Compression.Gzip) as channel:  # Gzip 압축 사용
        stub = example_pb2_grpc.DataServiceStub(channel)
        response = stub.GetData(example_pb2.DataRequest(data_id="1"))

        print(f"{response.data}")  # 압축 해제된 데이터 크기 출력

if __name__ == '__main__':
    run()