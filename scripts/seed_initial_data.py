import sys
sys.path.insert(0, '/app')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash
import os
import json

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    sys.exit(1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def seed_data():
    db = SessionLocal()
    
    try:
        print("🌱 Seeding initial data...")
        
        # 1. System Admin
        result = db.execute(text("SELECT COUNT(*) FROM system_admins WHERE email = 'hamed.niavand@gmail.com'"))
        if result.scalar() == 0:
            hashed = get_password_hash("admin123")
            db.execute(text("""
                INSERT INTO system_admins (email, hashed_password, name, is_active)
                VALUES (:email, :password, :name, :active)
            """), {"email": "hamed.niavand@gmail.com", "password": hashed, "name": "Hamed Niavand", "active": True})
            print("✓ System admin created")
        else:
            print("✓ System admin already exists")
        
        # 2. Demo Company
        result = db.execute(text("SELECT id FROM companies WHERE name = 'Demo Corp'"))
        company = result.first()
        if not company:
            db.execute(text("""
                INSERT INTO companies (name, plan_limits, is_active)
                VALUES (:name, :limits::jsonb, :active)
            """), {"name": "Demo Corp", "limits": json.dumps({"max_users": 200, "max_storage_gb": 100}), "active": True})
            result = db.execute(text("SELECT id FROM companies WHERE name = 'Demo Corp'"))
            company_id = result.scalar()
            print(f"✓ Demo company created (ID: {company_id})")
        else:
            company_id = company[0]
            print(f"✓ Demo company exists (ID: {company_id})")
        
        # 3. Default Roles
        roles = [
            ("Admin", {"can_manage_users": True, "can_manage_docs": True, "can_view_analytics": True}),
            ("Department Lead", {"can_manage_docs": True, "can_create_templates": True}),
            ("Employee", {"can_view_docs": True, "can_search": True})
        ]
        
        for role_name, perms in roles:
            result = db.execute(text("SELECT COUNT(*) FROM roles WHERE company_id = :cid AND name = :name"), 
                              {"cid": company_id, "name": role_name})
            if result.scalar() == 0:
                db.execute(text("""
                    INSERT INTO roles (company_id, name, permissions)
                    VALUES (:cid, :name, :perms::jsonb)
                """), {"cid": company_id, "name": role_name, "perms": json.dumps(perms)})
        print("✓ Default roles created")
        
        # 4. Case Templates
        templates = [
            {
                "name": "Post-Mortem Analysis",
                "sections": ["Overview", "Timeline", "Root Cause Analysis", "Impact Assessment", "Lessons Learned", "Action Items"]
            },
            {
                "name": "Client Project Summary",
                "sections": ["Client Information", "Project Objectives", "Deliverables", "Timeline", "Outcomes", "Next Steps"]
            },
            {
                "name": "Product Launch Review",
                "sections": ["Product Overview", "Launch Strategy", "Key Metrics", "Customer Feedback", "Lessons", "Future Improvements"]
            }
        ]
        
        for tpl in templates:
            result = db.execute(text("SELECT COUNT(*) FROM case_templates WHERE name = :name AND is_default = TRUE"), 
                              {"name": tpl["name"]})
            if result.scalar() == 0:
                tpl_json = json.dumps({"sections": tpl["sections"]})
                db.execute(text("""
                    INSERT INTO case_templates (name, template_json, is_default)
                    VALUES (:name, :json::jsonb, TRUE)
                """), {"name": tpl["name"], "json": tpl_json})
        print("✓ Default case templates created")
        
        db.commit()
        
        print("\n" + "="*50)
        print("✅ Database initialization complete!")
        print("="*50)
        print("\n📝 System Admin Credentials:")
        print("   Email:    hamed.niavand@gmail.com")
        print("   Password: admin123")
        print("\n⚠️  IMPORTANT: Change this password immediately!")
        print("\n📊 Initial Data:")
        print("   • 1 System Admin")
        print("   • 1 Company (Demo Corp)")
        print("   • 3 Roles")
        print("   • 3 Case Templates")
        print("="*50 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()