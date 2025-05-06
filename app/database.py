from sqlmodel import create_engine, SQLModel, Session

# DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/kurvalf"
DATABASE_URL = "postgresql+psycopg2://postgres:password@103.171.85.26:5432/kurvalf"

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True,connect_args={
                  "keepalives": 1,
                  "keepalives_idle": 30,
                  "keepalives_interval": 10,
                  "keepalives_count": 5,
              },)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session