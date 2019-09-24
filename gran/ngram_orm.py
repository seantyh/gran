from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Index

Base = declarative_base()

class NGram(Base):
    __tablename__ = 'ngram'

    id = Column(Integer, primary_key=True)
    ngram = Column('ngram', String, index=True)
    ncharac = Column('ncharac', Integer, index=True)
    freq = Column('freq', Integer)
    delim = Column('delim', String)
    
    def __repr__(self):
        return f"<NGram: {self.ngram}, {self.freq}>"
    