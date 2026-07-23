from database import engine
from models import Base
from email_log_models import EmailLog

# Import all models so SQLAlchemy registers them
import models
import tracking_models
import campaign_models
import template_models
import admin_models
import email_status_models

Base.metadata.create_all(bind=engine)

print("All tables created successfully!")