import grpc
from concurrent import futures
import logging
from generated import glossary_pb2, glossary_pb2_grpc
from grpc_reflection.v1alpha import reflection
from service import GlossaryService
from database import init_db

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    service = GlossaryService()
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(service, server)
    
    SERVICE_NAMES = (
        glossary_pb2.DESCRIPTOR.services_by_name['GlossaryService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    
    logging.info("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_db()
    serve() 