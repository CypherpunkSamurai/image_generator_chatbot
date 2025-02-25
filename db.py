from typing import List, Dict
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.sql import func

# Initialize SQLAlchemy
Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String)
    role = Column(String)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DatabaseMemory:
    def __init__(self, db_url: str = "sqlite:///chat_history.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        
    def save_message(self, conversation_id: str, role: str, content: str):
        with Session(self.engine) as session:
            message = ChatMessage(
                id=f"{conversation_id}_{datetime.now().timestamp()}",
                conversation_id=conversation_id,
                role=role,
                content=content
            )
            session.add(message)
            session.commit()
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        with Session(self.engine) as session:
            messages = session.query(ChatMessage)\
                .filter(ChatMessage.conversation_id == conversation_id)\
                .order_by(ChatMessage.created_at)\
                .all()
            return [{"role": msg.role, "content": msg.content} for msg in messages]
