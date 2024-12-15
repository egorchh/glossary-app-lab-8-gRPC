import grpc
from generated import glossary_pb2, glossary_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = glossary_pb2_grpc.GlossaryServiceServicer(channel)
        
        # Пример создания термина
        term = stub.CreateTerm(glossary_pb2.CreateTermRequest(
            term="gRPC",
            description="Высокопроизводительный фреймворк для RPC"
        ))
        print(f"Created term: {term.term}")
        
        # Пример получения списка терминов
        response = stub.ListTerms(glossary_pb2.ListTermsRequest(
            skip=0,
            limit=10
        ))
        print(f"Total terms: {response.total}")
        for term in response.terms:
            print(f"- {term.term}: {term.description}")
        
        # Пример поиска терминов
        search_request = glossary_pb2.SearchTermsRequest(query="gRPC")
        for term in stub.SearchTerms(search_request):
            print(f"Found: {term.term}")

if __name__ == '__main__':
    run() 