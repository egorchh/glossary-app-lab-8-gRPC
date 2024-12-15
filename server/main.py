import grpc
from concurrent import futures
import logging
from generated import glossary_pb2_grpc
from service import GlossaryService
from database import init_db

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(
        GlossaryService(), server
    )
    
    server.add_insecure_port('[::]:50051')
    server.start()
    
    logging.info("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_db()
    serve() 