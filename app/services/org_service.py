from fastapi import HTTPException, status
from app.db.database import db
from app.schemas.payload import OrgCreate, OrgUpdate
from app.core.security import get_password_hash

class OrganizationService:
    @staticmethod
    async def create_organization(self, payload: OrgCreate):
        # DEBUG: Verify what we received
        if len(payload.password) < 73:
             # Should be fine, but let's prove it
             pass
        else:
             # This should have been caught by Pydantic
             raise ValueError(f"Password too long in Service! Len: {len(payload.password)}")

        # Check existing
        existing_org = await db.get_db()["organizations"].find_one({"email": payload.email})
        if existing_org:
            raise HTTPException(status_code=400, detail="Organization name already taken")
        
        existing_user = await db.get_db()["users"].find_one({"email": payload.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # 2. Create Admin User & Save Meta
        hashed_password = get_password_hash(payload.password)
        
        # Transaction-like sequence (MongoDB 4.0+ supports transactions, but keeping it simple for async motor)
        # Save Org Metadata
        org_data = {
            "name": payload.name,
            "collection_name": f"org_{payload.name}",
            "connection_uri": "default_cluster"  # identifying which cluster this tenant lives in
        }
        await db.get_db()["organizations"].insert_one(org_data)

        # Save Admin User
        user_data = {
            "email": payload.email,
            "password": hashed_password,
            "org_name": payload.name,
            "role": "admin"
        }
        await db.get_db()["users"].insert_one(user_data)

        # 3. Create Dynamic Collection
        # In Mongo, creating a document in a non-existent collection creates it, 
        # but we can explicitly create it to ensure it exists for the tenant.
        try:
            await db.get_dynamic_collection(org_data["collection_name"]).insert_one({"info": "tenant_initialized"})
        except Exception as e:
            # Rollback logic would go here in a real prod env
            pass

        return {"message": "Organization created successfully", "org": payload.name}

    @staticmethod
    async def update_organization(current_name: str, payload: OrgUpdate):
        # 1. Check new name availability
        if await db.get_db()["organizations"].find_one({"name": payload.name}):
            raise HTTPException(status_code=400, detail="New organization name already taken")

        # 2. Rename Collection (Migration)
        old_collection_name = f"org_{current_name}"
        new_collection_name = f"org_{payload.name}"
        
        try:
            # Rename the actual collection in MongoDB
            await db.get_dynamic_collection(old_collection_name).rename(new_collection_name)
        except Exception:
            # If collection didn't exist for some reason, just proceed (or handle error)
            pass

        # 3. Update Meta
        await db.get_db()["organizations"].update_one(
            {"name": current_name},
            {"$set": {"name": payload.name, "collection_name": new_collection_name}}
        )

        # 4. Update User
        await db.get_db()["users"].update_many(
            {"org_name": current_name},
            {"$set": {"org_name": payload.name}}
        )
        
        return {"message": "Organization updated successfully", "new_name": payload.name}
