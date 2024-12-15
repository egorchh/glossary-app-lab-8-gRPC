import grpc
from generated import glossary_pb2, glossary_pb2_grpc
import logging

def run():
    # Устанавливаем соединение с сервером
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = glossary_pb2_grpc.GlossaryServiceStub(channel)
        
        try:
            # 1. Создание термина
            print("\n=== Создание термина ===")
            term = stub.CreateTerm(glossary_pb2.CreateTermRequest(
                term="gRPC",
                description="Высокопроизводительный фреймворк для RPC"
            ))
            print(f"Создан термин: {term.term} - {term.description}")
            
            # 2. Получение списка терминов
            print("\n=== Список терминов ===")
            response = stub.ListTerms(glossary_pb2.ListTermsRequest(
                skip=0,
                limit=10
            ))
            print(f"Всего терминов: {response.total}")
            for term in response.terms:
                print(f"- {term.term}: {term.description}")
            
            # 3. Получение термина по названию
            print("\n=== Получение термина ===")
            term = stub.GetTerm(glossary_pb2.GetTermRequest(term="gRPC"))
            print(f"Найден термин: {term.term} - {term.description}")
            
            # 4. Обновление термина
            print("\n=== Обновление термина ===")
            updated_term = stub.UpdateTerm(glossary_pb2.UpdateTermRequest(
                term="gRPC",
                description="Обновленное описание gRPC"
            ))
            print(f"Обновлен термин: {updated_term.term} - {updated_term.description}")
            
            # 5. Поиск терминов
            print("\n=== Поиск терминов ===")
            search_request = glossary_pb2.SearchTermsRequest(query="gRPC")
            for term in stub.SearchTerms(search_request):
                print(f"Найдено: {term.term} - {term.description}")
            
            # 6. Удаление термина
            print("\n=== Удаление термина ===")
            delete_response = stub.DeleteTerm(glossary_pb2.DeleteTermRequest(term="gRPC"))
            print(f"Результат удаления: {delete_response.message}")

        except grpc.RpcError as e:
            print(f"Ошибка RPC: {e.details()}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run() 