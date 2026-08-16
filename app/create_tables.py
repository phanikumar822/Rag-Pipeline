from app.database import engine, Base
from app.models.documents import Document

Base.metadata.create_all(engine)

print("Tables created")