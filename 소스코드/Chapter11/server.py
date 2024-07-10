from concurrent import futures
import grpc
import time
import cancel_example_pb2
import cancel_example_pb2_grpc

# 서버 측 서비스 구현
class CancelServiceServicer(cancel_example_pb2_grpc.CancelServiceServicer):
    # LongRunningOperation 메서드 구현
    def LongRunningOperation(self, request, context):
        for i in range(2):
            # 요청이 활성 상태인지 확인
            if context.is_active():
                print(f"Processing {i}...")
                time.sleep(5)  # 실제 작업을 시뮬레이션하는 지연 시간
            else:
                # 요청이 취소되었을 때
                print("Request was cancelled")
                return cancel_example_pb2.Response(response_data="Cancelled")
        # 작업이 완료되었을 때
        return cancel_example_pb2.Response(response_data="Completed")

def serve():
    # gRPC 서버 생성
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 서비스 추가
    cancel_example_pb2_grpc.add_CancelServiceServicer_to_server(CancelServiceServicer(), server)
    # 서버 포트 설정
    server.add_insecure_port('[::]:50051')
    # 서버 시작
    server.start()
    # 서버 종료를 기다림
    server.wait_for_termination()

if __name__ == '__main__':
    serve()