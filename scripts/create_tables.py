import sys
sys.path.insert(0, '/app')

from app.core.database import engine, Base
from app.models.models import (
    SystemAdmin, Company, Role, Department, User, 
    Document, DocumentChunk, CaseTemplate, CaseInstance,
    OnboardingPath, SearchHistory, ActivityLog
)

print("Creating database tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")
except Exception as e:
    print(f"❌ Error creating tables: {e}")
    import traceback
    traceback.print_exc()
