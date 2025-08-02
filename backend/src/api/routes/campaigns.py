# backend/src/api/routes/campaigns.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
import io

from ...core.database import get_db
from ...models import campaign as campaign_model
from ...schemas import campaign as campaign_schema

router = APIRouter()

@router.post("/", response_model=campaign_schema.Campaign, status_code=status.HTTP_201_CREATED)
def create_campaign(campaign: campaign_schema.CampaignCreate, db: Session = Depends(get_db)):
    db_campaign = campaign_model.Campaign(name=campaign.name, agent_id=campaign.agent_id)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

@router.get("/", response_model=List[campaign_schema.Campaign])
def read_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    campaigns = db.query(campaign_model.Campaign).offset(skip).limit(limit).all()
    return campaigns
    
@router.get("/{campaign_id}", response_model=campaign_schema.Campaign)
def read_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign

@router.post("/{campaign_id}/contacts", status_code=status.HTTP_201_CREATED)
async def add_contacts_from_csv(campaign_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    contents = await file.read()
    file_like_object = io.StringIO(contents.decode())
    csv_reader = csv.DictReader(file_like_object)

    contacts_to_add = []
    for row in csv_reader:
        # Assuming the CSV has a column named 'phone_number'
        phone_number = row.get('phone_number')
        if phone_number:
            contacts_to_add.append(campaign_model.Contact(
                phone_number=phone_number,
                campaign_id=campaign_id
            ))
    
    if not contacts_to_add:
        raise HTTPException(status_code=400, detail="CSV must contain a 'phone_number' column with valid data.")
    
    db.add_all(contacts_to_add)
    db.commit()

    return {"message": f"{len(contacts_to_add)} contacts added to campaign {campaign_id}"}

# NOTE: The 'start' and 'stop' endpoints are placeholders for now.
# A real implementation requires an async task queue like Celery.
@router.post("/{campaign_id}/start")
def start_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    db_campaign.status = "running"
    db.commit()
    
    # In a real app, you would trigger an async task here:
    # start_calling_task.delay(campaign_id)
    
    return {"message": f"Campaign {campaign_id} started. (This is a simulation)"}
    
@router.post("/{campaign_id}/stop")
def stop_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    db_campaign.status = "paused"
    db.commit()
    
    
    return {"message": f"Campaign {campaign_id} stopped."}

@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    db.delete(db_campaign)
    db.commit()
    
    return