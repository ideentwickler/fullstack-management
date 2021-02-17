import typing as t

from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app import crud, models

db = SessionLocal()
CalcType = t.NewType('Calculation Type', str)


def get_claim_bill(
        _db: Session = db, *, start: datetime = None, end: datetime = None,
        store_internal_id: int = None, owner_id: int = None,
        kind: models.ClaimKind = None, calculation: CalcType = "avg"
):
    """ WE USE THIS FUNCTION TO CREATE A CLAIM QUERY WITH OPTIONAL PARAMETER
        AND CALCULATE BY SQLALCHEMY.SQL.FUNC
    """
    query = crud.claim.get_query(_db)
    if start and end:
        query = query.filter(models.Claim.created_at.between(start, end))
    if store_internal_id:
        query = query.filter(models.Claim.store_internal_id == store_internal_id)
    if owner_id:
        query = query.filter(models.Claim.owner_id == owner_id)
    if kind:
        query = query.filter(models.Claim.kind == kind)
    bill = query.with_entities(getattr(func, calculation)(models.Claim.bill).label("_bill")).first()
    bill_round = round(bill[0], 2) if bill[0] is not None else 0.00
    return bill_round


def get_clean_discharge(
        _db: Session = db, *, start: datetime = None, end: datetime = None,
        store_internal_id: int = None, owner_id: int = None
) -> float:
    """
    TO AVOID MULTIPLE COUNTED DISCHARGES
    WE ONLY ACCEPT ONE DISCHARGE PER CONTRACT
    MEANS WE VE TO EXCLUDE ALL OTHER ROWS WITH THE SAME CONTRACT NR
    """
    exclude_contracts: t.List[int] = []
    discharges: t.List[float] = []
    claims = crud.claim.get_query(_db)
    if start and end:
        claims = claims.filter(models.Claim.created_at.between(start, end))  # noqa
    if store_internal_id:
        claims = claims.filter(models.Claim.store_internal_id == store_internal_id)  # noqa
    if owner_id:
        claims = claims.filter(models.Claim.owner_id == owner_id)  # noqa
    #  FOR BETTER SQL PERFORMANCE WE ENCLOSE OUR QUERY: EXCLUDE ALL WITH DISCHARGE IS NULL;
    claims = claims.filter(models.Claim.discharge.isnot(None))  # noqa
    claims: t.List[models.Claim] = claims.all()  # noqa

    for claim in claims:
        if claim.contract_nr not in exclude_contracts:
            exclude_contracts.append(claim.contract_nr)
            discharges.append(claim.discharge)
    total_discharges: float = sum(discharges)
    total_discharges_round: float = round(total_discharges, 2)
    return total_discharges_round
