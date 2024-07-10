import grpc
from concurrent import futures
import cv2
import videostreaming_pb2
import videostreaming_pb2_grpc

class VideoStreamingServiceServicer(videostreaming_pb2_grpc.VideoStreamingServiceServicer):
    def StreamVideo(self, request, context):
        video_path = request.video_name
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            context.set_details('Video file not found or cannot be opened')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                _, buffer = cv2.imencode('.jpg', frame)
                video_frame = buffer.tobytes()
                yield videostreaming_pb2.VideoFrame(frame=video_frame)
        finally:
            cap.release()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    videostreaming_pb2_grpc.add_VideoStreamingServiceServicer_to_server(VideoStreamingServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
