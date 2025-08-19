import json
from datetime import datetime, timezone, timedelta
from sqlalchemy import insert
from ..db import AsyncSessionLocal
from ..models import Order, Source

# NOTE: This is a sample ingester to prove the pipeline; replace with real NSE/BSE crawlers later.

async def ingest_sample():
    with open(__file__.replace("crawler.py", "sample_data.json"), "r", encoding="utf-8") as f:
        items = json.load(f)

    async with AsyncSessionLocal() as session:
        for it in items:
            await upsert_order(session, it)
        await session.commit()

async def upsert_order(session, it: dict):
    # Upsert by natural key (company + timestamp + value)
    exists = await session.execute(
        '''
        select id from orders
        where company_name = :c and announcement_time_ist = :t
          and coalesce(order_value_inr, -1) = coalesce(:v, -1)
        limit 1
        ''',
        {"c": it["company_name"], "t": datetime.fromisoformat(it["announcement_time_ist"]), "v": it.get("order_value_inr")},
    )
    if exists.first():
        return

    # IST now
    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    ann_ts = datetime.fromisoformat(it["announcement_time_ist"])
    ann_date = ann_ts.date()  # YYYY-MM-DD part (already IST if timestamp had +05:30)

    res = await session.execute(
        insert(Order).values(
            company_name=it["company_name"],
            symbol=it.get("symbol"),
            isin=it.get("isin"),
            exchange=it.get("exchange"),
            sector=it.get("sector"),
            business_unit=it.get("business_unit"),
            geography=it.get("geography"),
            order_value_inr=it.get("order_value_inr"),
            currency_original=it.get("currency_original"),
            original_value_text=it.get("original_value"),
            value_confidence=it.get("value_confidence"),
            client_name=it.get("client_name"),
            order_type=it.get("order_type"),
            duration_text=it.get("duration"),
            announcement_time_ist=ann_ts,
            announcement_date_ist=ann_date,
            materiality_flag=None,
            confidence_score=None,
            created_at=now,
            updated_at=now,
        ).returning(Order.id)
    )
    oid = res.scalar()

    if it.get("source_url"):
        await session.execute(
            insert(Source).values(
                order_id=oid,
                source_type=it.get("source_type", "NSE"),
                source_url=it["source_url"],
                pdf_url=it.get("pdf_url"),
            )
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(ingest_sample())
