from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend import schemas, models, auth
from backend.database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.OrderOut)
async def create_order(
    order_data: schemas.OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != models.UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Только студенты могут создавать заявки")
    order = models.Order(
        user_id=current_user.id,
        certificate_type=order_data.certificate_type,
        reason=order_data.reason
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    order.user = current_user
    return order

@router.get("/", response_model=list[schemas.OrderOut])
async def list_orders(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = select(models.Order).where(models.Order.user_id == current_user.id).order_by(models.Order.created_at.desc())
    if current_user.role == models.UserRole.STAFF:
        query = select(models.Order).order_by(models.Order.created_at.desc())
    result = await db.execute(query)
    orders = result.scalars().all()
    return orders

@router.patch("/{order_id}/status", response_model=schemas.OrderOut)
async def change_status(
    order_id: int,
    new_status: models.OrderStatus,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != models.UserRole.STAFF:
        raise HTTPException(status_code=403, detail="Только сотрудники могут менять статус")
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    order.status = new_status
    await db.commit()
    await db.refresh(order)
    order.user = current_user
    return order