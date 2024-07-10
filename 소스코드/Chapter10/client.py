import grpc
import cv2
import numpy as np
import videostreaming_pb2
import videostreaming_pb2_grpc

def stream_video_frames(video_frames):
    for frame in video_frames:
        np_data = np.frombuffer(frame.frame, dtype=np.uint8)
        video = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        if video is not None:
            cv2.imshow('Video', video)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = videostreaming_pb2_grpc.VideoStreamingServiceStub(channel)
        video_name = 'test.mp4'  # 요청할 비디오 파일 경로
        video_request = videostreaming_pb2.VideoRequest(video_name=video_name)
        video_frames = stub.StreamVideo(video_request)
        stream_video_frames(video_frames)

if __name__ == '__main__':
    run()
