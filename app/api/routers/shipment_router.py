from fastapi import APIRouter, HTTPException, status
from app.api.dependencies import SellerDep, ServiceDep,PartnerDep
from app.api.schema.shipment import ShipmentCreateSchema, ShipmentUpdateSchema, ShipmentResponseSchema
from app.api.dependencies import SellerDep
import uuid
router = APIRouter()

@router.get("/shipment", response_model=ShipmentResponseSchema)
async def get_shipment(id:uuid.UUID, service : ServiceDep, seller: SellerDep):
    shipment = await service.get(id)
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipment


@router.post("/shipment", response_model=ShipmentResponseSchema)
async def create_shipment(service: ServiceDep, shipment: ShipmentCreateSchema, seller: SellerDep):
    return await service.add(shipment,seller)
    

@router.patch("/shipment/{id}")
async def update_shipment(id:uuid.UUID, service: ServiceDep, partner: PartnerDep, shipment_update:ShipmentUpdateSchema):
    update = shipment_update.model_dump(exclude_unset=True)

    if not update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    
    return await service.update(id, update)

@router.delete("/shipment/{id}")
async def delete_shipment(id:uuid.UUID, service:ServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"message": f"Shipment  with {id} deleted successfully"}
