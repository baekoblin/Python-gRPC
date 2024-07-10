import grpc
import cancel_example_pb2
import cancel_example_pb2_grpc
import time

def run():
    # 서버와의 채널 생성
    with grpc.insecure_channel('localhost:50051') as channel:
        # Stub 생성
        stub = cancel_example_pb2_grpc.CancelServiceStub(channel)
        request = cancel_example_pb2.Request(request_data="Start")
        
        # 비동기 호출 시작
        future = stub.LongRunningOperation.future(request)
        
        # 일정 시간 후 요청 취소
        time.sleep(3)
        future.cancel()
        
        try:
            # 응답 받기 시도
            response = future.result()
            print(f"Response received: {response.response_data}")
        except grpc.FutureCancelledError:
            # 요청이 취소된 경우
            print("Request was cancelled.")

if __name__ == '__main__':
    run()