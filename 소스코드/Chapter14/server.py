from concurrent import futures
import grpc
import error_handling_example_pb2
import error_handling_example_pb2_grpc

class CalculatorServicer(error_handling_example_pb2_grpc.CalculatorServicer):
    def Divide(self, request, context):
        if request.divisor == 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Divisor cannot be zero.")
            return error_handling_example_pb2.DivideResponse()
        quotient = request.dividend / request.divisor
        return error_handling_example_pb2.DivideResponse(quotient=quotient)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    error_handling_example_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()