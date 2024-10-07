from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from classes import Base, Track, User, Listen_history

# parameter: check for primary key duplicates before insertion (takes longer but ensures data quality)
check_PK_double = True

# parameter: output log of the SQLalchemy queries
output_SQL_to_console = False

def load(data):
    # create the SQL engine database and tables
    engine = create_engine("sqlite:///mydb.db", echo=output_SQL_to_console)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    for items in data:
        if check_PK_double:
            with session.no_autoflush:
                for item in items:
                    if isinstance(item, Track):
                        q = session.query(Track).filter(Track.id==item.id)
                        if not session.query(q.exists()).scalar():
                            session.add(item)

                    elif isinstance(item, User):
                        q = session.query(User).filter(User.id==item.id)
                        if not session.query(q.exists()).scalar():
                            session.add(item)

                    elif isinstance(item, Listen_history):
                        q = session.query(Listen_history).filter(Listen_history.user_id==item.user_id).filter(Listen_history.track_id==item.track_id)
                        if not session.query(q.exists()).scalar():
                            session.add(item)
        
        else:
            for item in items:
                session.add(item)
    
    session.commit()

    return session