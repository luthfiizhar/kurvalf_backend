from sqlmodel import create_engine, SQLModel, Session

# DATABASE_URL = "postgresql+psycopg2://postgres:password@host.docker.internal:5432/kurvalf"
DATABASE_URL = "postgresql+psycopg2://postgres:P@ssw0rd.99@103.171.85.26:5432/kurvalf"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session