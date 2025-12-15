from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from app.db import SessionLocal
from app.fastapi_auth import require_auth
from app.models.accounting import Account, AccountType, JournalEntry, JournalLine, Currency, ExchangeRate

router = APIRouter()

def get_session():
    return SessionLocal()

# Accounts
@router.get("/accounts")
async def list_accounts(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Account).order_by(Account.code)).scalars().all()
        return [
            {"id": a.id, "code": a.code, "name": a.name, "type": a.type.value, "parent_id": a.parent_id}
            for a in rows
        ]

@router.post("/accounts")
async def create_account(payload: dict, _: dict = Depends(require_auth)):
    code = payload.get("code"); name = payload.get("name"); type_ = payload.get("type")
    if not code or not name or not type_:
        raise HTTPException(status_code=400, detail="code, name, type required")
    try:
        acct_type = AccountType(type_)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid account type")
    a = Account(code=code, name=name, type=acct_type, parent_id=payload.get("parent_id"))
    with get_session() as db:
        db.add(a); db.commit(); db.refresh(a)
        return {"id": a.id, "code": a.code, "name": a.name, "type": a.type.value}

# Journal entries
@router.get("/journal")
async def list_journal(_: dict = Depends(require_auth)):
    with get_session() as db:
        entries = db.execute(select(JournalEntry).order_by(JournalEntry.posted_at.desc())).scalars().all()
        result = []
        for e in entries:
            lines = [
                {
                    "id": l.id,
                    "account_id": l.account_id,
                    "description": l.description,
                    "debit": float(l.debit),
                    "credit": float(l.credit),
                } for l in e.lines
            ]
            result.append({
                "id": e.id,
                "ref": e.ref,
                "memo": e.memo,
                "posted_at": str(e.posted_at),
                "currency_id": e.currency_id,
                "lines": lines,
            })
        return result

@router.post("/journal")
async def create_entry(payload: dict, _: dict = Depends(require_auth)):
    lines = payload.get("lines", [])
    if not lines or not isinstance(lines, list):
        raise HTTPException(status_code=400, detail="lines required")
    e = JournalEntry(ref=payload.get("ref"), memo=payload.get("memo"), currency_id=payload.get("currency_id"))
    with get_session() as db:
        db.add(e)
        for ln in lines:
            jl = JournalLine(entry=e,
                             account_id=ln.get("account_id"),
                             description=ln.get("description"),
                             debit=ln.get("debit", 0),
                             credit=ln.get("credit", 0))
            if jl.account_id is None:
                raise HTTPException(status_code=400, detail="account_id required on line")
            db.add(jl)
        # Validate double-entry: sum(debit) == sum(credit)
        db.flush()
        totals = db.execute(select(func.sum(JournalLine.debit), func.sum(JournalLine.credit)).where(JournalLine.entry_id == e.id)).one()
        if float(totals[0] or 0) != float(totals[1] or 0):
            raise HTTPException(status_code=400, detail="debits must equal credits")
        db.commit(); db.refresh(e)
        return {"id": e.id, "ref": e.ref, "memo": e.memo}

# Reports (basic placeholders)
@router.get("/reports/pl")
async def profit_and_loss(_: dict = Depends(require_auth)):
    # Sum revenue - expense
    with get_session() as db:
        revenue_ids = [a.id for a in db.execute(select(Account).where(Account.type == AccountType.REVENUE)).scalars().all()]
        expense_ids = [a.id for a in db.execute(select(Account).where(Account.type == AccountType.EXPENSE)).scalars().all()]
        rev = db.execute(select(func.sum(JournalLine.credit) - func.sum(JournalLine.debit)).where(JournalLine.account_id.in_(revenue_ids))).scalar() or 0
        exp = db.execute(select(func.sum(JournalLine.debit) - func.sum(JournalLine.credit)).where(JournalLine.account_id.in_(expense_ids))).scalar() or 0
        return {"revenue": float(rev), "expenses": float(exp), "profit": float(rev) - float(exp)}

@router.get("/reports/balance_sheet")
async def balance_sheet(_: dict = Depends(require_auth)):
    with get_session() as db:
        def balance_for(t):
            acc_ids = [a.id for a in db.execute(select(Account).where(Account.type == t)).scalars().all()]
            bal = db.execute(select(func.sum(JournalLine.debit) - func.sum(JournalLine.credit)).where(JournalLine.account_id.in_(acc_ids))).scalar() or 0
            return float(bal)
        return {
            "assets": balance_for(AccountType.ASSET),
            "liabilities": balance_for(AccountType.LIABILITY),
            "equity": balance_for(AccountType.EQUITY),
        }

@router.get("/currencies")
async def list_currencies(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Currency).order_by(Currency.code)).scalars().all()
        return [{"id": c.id, "code": c.code, "name": c.name, "symbol": c.symbol} for c in rows]

@router.post("/currencies")
async def create_currency(payload: dict, _: dict = Depends(require_auth)):
    code = payload.get("code"); name = payload.get("name")
    if not code or not name:
        raise HTTPException(status_code=400, detail="code and name required")
    c = Currency(code=code, name=name, symbol=payload.get("symbol"))
    with get_session() as db:
        db.add(c); db.commit(); db.refresh(c)
        return {"id": c.id, "code": c.code, "name": c.name, "symbol": c.symbol}
