from generated import glossary_pb2, glossary_pb2_grpc
from database import SessionLocal
from models import Term
import grpc

class GlossaryService(glossary_pb2_grpc.GlossaryServiceServicer):
    def ListTerms(self, request, context):
        with SessionLocal() as db:
            terms = db.query(Term).offset(request.skip).limit(request.limit).all()
            total = db.query(Term).count()
            
            return glossary_pb2.ListTermsResponse(
                terms=[
                    glossary_pb2.Term(
                        id=term.id,
                        term=term.term,
                        description=term.description
                    ) for term in terms
                ],
                total=total
            )
    
    def GetTerm(self, request, context):
        with SessionLocal() as db:
            term = db.query(Term).filter(Term.term == request.term).first()
            if not term:
                context.abort(grpc.StatusCode.NOT_FOUND, 'Термин не найден')
            
            return glossary_pb2.Term(
                id=term.id,
                term=term.term,
                description=term.description
            )
    
    def CreateTerm(self, request, context):
        with SessionLocal() as db:
            if db.query(Term).filter(Term.term == request.term).first():
                context.abort(grpc.StatusCode.ALREADY_EXISTS, 'Термин уже существует')
            
            term = Term(term=request.term, description=request.description)
            db.add(term)
            db.commit()
            db.refresh(term)
            
            return glossary_pb2.Term(
                id=term.id,
                term=term.term,
                description=term.description
            )
    
    def UpdateTerm(self, request, context):
        with SessionLocal() as db:
            term = db.query(Term).filter(Term.term == request.term).first()
            if not term:
                context.abort(grpc.StatusCode.NOT_FOUND, 'Термин не найден')
            
            term.description = request.description
            db.commit()
            db.refresh(term)
            
            return glossary_pb2.Term(
                id=term.id,
                term=term.term,
                description=term.description
            )
    
    def DeleteTerm(self, request, context):
        with SessionLocal() as db:
            term = db.query(Term).filter(Term.term == request.term).first()
            if not term:
                context.abort(grpc.StatusCode.NOT_FOUND, 'Термин не найден')
            
            db.delete(term)
            db.commit()
            
            return glossary_pb2.DeleteTermResponse(
                success=True,
                message='Термин успешно удален'
            )
    
    def SearchTerms(self, request, context):
        with SessionLocal() as db:
            terms = db.query(Term).filter(
                Term.term.ilike(f"%{request.query}%")
            ).all()
            
            for term in terms:
                yield glossary_pb2.Term(
                    id=term.id,
                    term=term.term,
                    description=term.description
                ) 