import grpc
from concurrent import futures
import streaming_pb2
import streaming_pb2_grpc

# 서비스 구현
class StreamingServiceServicer(streaming_pb2_grpc.StreamingServiceServicer):
    def StreamData(self, request_iterator, context):
        # 클라이언트로부터 스트리밍 데이터를 처리하는 부분
        result = ""
        for req in request_iterator:
            # 각 요청의 데이터를 result에 추가
            result += req.data + " "
        # 최종 결과 반환
        return streaming_pb2.ResponseMessage(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()