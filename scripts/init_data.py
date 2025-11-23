import sys
import os
sys.path.insert(0, '/app')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash
from app.models.models import Base, SystemAdmin, Company, Role, CaseTemplate
from datetime import datetime

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    sys.exit(1)

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    db = SessionLocal()
    
    try:
        print("🔄 Initializing database...")
        
        # 1. Create System Admin
        admin_exists = db.query(SystemAdmin).filter_by(email="hamed.niavand@gmail.com").first()
        if not admin_exists:
            admin = SystemAdmin(
                email="hamed.niavand@gmail.com",
                hashed_password=get_password_hash("admin123"),
                name="Hamed Niavand",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("✓ System admin created")
        else:
            print("✓ System admin already exists")
        
        # 2. Create Demo Company
        company_exists = db.query(Company).filter_by(name="Demo Corp").first()
        if not company_exists:
            company = Company(
                name="Demo Corp",
                domain_restriction=None,
                plan_limits={"max_users": 200, "max_storage_gb": 100},
                is_active=True
            )
            db.add(company)
            db.commit()
            db.refresh(company)
            company_id = company.id
            print(f"✓ Demo company created (ID: {company_id})")
        else:
            company_id = company_exists.id
            print(f"✓ Demo company already exists (ID: {company_id})")
        
        # 3. Create Default Roles
        role_names = ["Admin", "Department Lead", "Employee"]
        for role_name in role_names:
            role_exists = db.query(Role).filter_by(company_id=company_id, name=role_name).first()
            if not role_exists:
                role = Role(
                    company_id=company_id,
                    name=role_name,
                    permissions={"can_manage_users": role_name == "Admin"}
                )
                db.add(role)
        db.commit()
        print("✓ Default roles created")
        
        # 4. Create Default Case Templates
        templates = [
            {
                "name": "Post-Mortem Analysis",
                "template_json": {
                    "sections": ["Overview", "Timeline", "Root Cause", "Impact", "Lessons Learned", "Action Items"]
                }
            },
            {
                "name": "Client Project Summary",
                "template_json": {
                    "sections": ["Client Info", "Objectives", "Deliverables", "Timeline", "Outcomes", "Next Steps"]
                }
            },
            {
                "name": "Product Launch Review",
                "template_json": {
                    "sections": ["Product Overview", "Launch Strategy", "Metrics", "Feedback", "Lessons", "Improvements"]
                }
            }
        ]
        
        for tpl in templates:
            template_exists = db.query(CaseTemplate).filter_by(name=tpl["name"], is_default=True).first()
            if not template_exists:
                template = CaseTemplate(
                    company_id=None,
                    name=tpl["name"],
                    template_json=tpl["template_json"],
                    is_default=True
                )
                db.add(template)
        db.commit()
        print("✓ Default case templates created")
        
        print("\n✅ Database initialization complete!")
        print("\n📝 System Admin Login:")
        print("   Email: hamed.niavand@gmail.com")
        print("   Password: admin123")
        print("   ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!\n")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
