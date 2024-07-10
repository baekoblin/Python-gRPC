import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc
import time

def run_check():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = health_pb2_grpc.HealthStub(channel)
        while True:
            response = stub.Check(health_pb2.HealthCheckRequest(service="my_service"))
            print(f"Health Check Status: {response.status}")
            time.sleep(2)

def run_watch():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = health_pb2_grpc.HealthStub(channel)
        responses = stub.Watch(health_pb2.HealthCheckRequest(service="my_service"))
        for response in responses:
            print(f"Health Watch Status: {response.status}")

if __name__ == '__main__':
    print("Running Check method:")
    run_check()
    # 또는
    # print("\nRunning Watch method:")
    # run_watch()
