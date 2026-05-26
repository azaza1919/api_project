from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine('postgresql://postgres:1234@localhost/mail')
Session = sessionmaker(bind=engine)

class aaa(DeclarativeBase):
    pass

class EmailSummary(aaa):
    __tablename__ = 'sum'

    email_id = Column(String, primary_key=True)
    subject  = Column(String) #тема письма
    summary  = Column(Text) #краткое содержание


'''запуск ДБ'''
def init_db():
    aaa.metadata.create_all(engine)

'''кэширование'''
def get_cached(email_id):
    with Session() as session:
        record = session.get(EmailSummary, email_id)
        return record.summary if record else None


'''сохранение'''
def save(email_id, subject, summary):
    with Session() as session:
        record = session.get(EmailSummary, email_id) or EmailSummary(email_id=email_id)
        record.subject = subject
        record.summary = summary
        session.merge(record)
        session.commit()