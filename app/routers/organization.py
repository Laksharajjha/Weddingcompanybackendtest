from fastapi import APIRouter, Depends, HTTPException
from app.schemas.payload import OrgCreate, OrgUpdate
from app.services.org_service import OrganizationService
from app.dependencies import get_current_user
from app.db.database import db

router = APIRouter()

@router.post("/organizations", status_code=201)
async def create_organization(payload: OrgCreate):
    return await OrganizationService.create_organization(payload)

@router.get("/organizations/me")
async def get_my_organization(current_user: dict = Depends(get_current_user)):
    org = await db.get_db()["organizations"].find_one({"name": current_user["org_name"]})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    # Convert ObjectId to str if needed or use a Pydantic model for response
    org["_id"] = str(org["_id"]) 
    return org

@router.put("/organizations/me")
async def update_my_organization(
    payload: OrgUpdate, 
    current_user: dict = Depends(get_current_user)
):
    return await OrganizationService.update_organization(current_user["org_name"], payload)

@router.delete("/organizations/me")
async def delete_my_organization(current_user: dict = Depends(get_current_user)):
    name = current_user["org_name"]
    org = await db.get_db()["organizations"].find_one({"name": name})
    if org:
        await db.get_db().drop_collection(org["collection_name"])
        await db.get_db()["organizations"].delete_one({"name": name})
        await db.get_db()["users"].delete_many({"org_name": name})
    return {"message": "Organization deleted"}
