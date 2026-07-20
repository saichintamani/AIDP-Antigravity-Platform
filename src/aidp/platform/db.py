from sqlalchemy import JSON, Column, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class ClaimRecord(Base):
    """
    SQLAlchemy Model representing an EpistemicClaim in the relational database.
    """
    __tablename__ = 'epistemic_claims'

    claim_id = Column(String, primary_key=True)
    claim_text = Column(Text, nullable=False)
    generated_by = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)
    
    # Store complex nested structures as JSON for flexibility, 
    # while maintaining relational integrity on the root claim.
    assumptions = Column(JSON, nullable=False, default=list)
    evidence = Column(JSON, nullable=False, default=list)
    confidence = Column(JSON, nullable=True)
    confidence_lineage = Column(JSON, nullable=False, default=list)
    reviewed_by = Column(JSON, nullable=False, default=list)
    verification_status = Column(String, nullable=False)
    
def get_engine(db_uri: str = "sqlite:///aidp_ledger.db"):
    """
    Creates and returns a SQLAlchemy engine.
    """
    engine = create_engine(db_uri, echo=False)
    Base.metadata.create_all(engine)
    return engine
    
def get_session_maker(engine):
    return sessionmaker(bind=engine)
