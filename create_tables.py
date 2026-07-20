from database import engine
from models import Base

# Import all models so SQLAlchemy registers them
import tracking_models
import campaign_models
import template_models

Base.metadata.create_all(bind=engine)

print("All tables created successfully!")