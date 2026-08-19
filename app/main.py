from fastapi import FastAPI, Depends, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import or_, desc, asc, func
from typing import List, Dict, Any, Optional

from app.database import get_db
from app.models import Mention
from app.cleaner import strip_html, normalize_source, parse_int, parse_datetime

app = FastAPI(
    title="Media Monitoring API",
    description="Backend service for ingestion, search, and analytics of mentions."
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Media Monitoring Service is running"}

# 1. BULK INGEST ENDPOINT
@app.post("/internal/mentions/bulk", status_code=status.HTTP_201_CREATED)
def bulk_ingest_mentions(payload: List[Dict[str, Any]], db: Session = Depends(get_db)):
    if not payload:
        return {"inserted": 0, "message": "Payload is empty"}

    cleaned_records = []
    for item in payload:
        url = item.get("url")
        if not url:
            continue

        cleaned = {
            "external_id": item.get("external_id"),
            "source": normalize_source(item.get("source")),
            "title": strip_html(item.get("title")),
            "content": strip_html(item.get("content")) or "",
            "url": url.strip(),
            "author": item.get("author"),
            "published_at": parse_datetime(item.get("published_at")),
            "engagement": parse_int(item.get("engagement")),
        }
        cleaned_records.append(cleaned)

    if not cleaned_records:
        return {"inserted": 0, "message": "No valid records to insert"}

    stmt = insert(Mention).values(cleaned_records)
    stmt = stmt.on_conflict_do_nothing(index_elements=['url'])
    
    result = db.execute(stmt)
    db.commit()

    return {
        "status": "success",
        "received": len(payload),
        "processed": len(cleaned_records),
        "inserted": result.rowcount,
        "message": "Bulk ingestion completed successfully."
    }

# 2. SEARCH & FILTER ENDPOINT
@app.get("/mentions")
def get_mentions(
    source: Optional[str] = Query(None, description="Filter berdasarkan source, e.g. instagram, the star"),
    q: Optional[str] = Query(None, description="Search keyword di title atau content"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("published_at", regex="^(published_at|engagement|created_at)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    query = db.query(Mention)

    if source:
        query = query.filter(Mention.source == source.strip().lower())

    if q:
        search_pattern = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Mention.title.ilike(search_pattern),
                Mention.content.ilike(search_pattern)
            )
        )

    total_items = query.count()

    sort_column = getattr(Mention, sort_by)
    if order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total_items": total_items,
        "total_pages": (total_items + limit - 1) // limit if limit > 0 else 0,
        "data": items
    }

# 3. STATS & ANALYTICS ENDPOINT
@app.get("/mentions/stats")
def get_mentions_stats(db: Session = Depends(get_db)):
    total_mentions = db.query(func.count(Mention.id)).scalar() or 0
    total_engagement = db.query(func.sum(Mention.engagement)).scalar() or 0

    # Breakdowns per source
    source_stats = (
        db.query(
            Mention.source,
            func.count(Mention.id).label("count"),
            func.sum(Mention.engagement).label("total_engagement")
        )
        .group_by(Mention.source)
        .all()
    )

    by_source = [
        {
            "source": row.source,
            "mentions_count": row.count,
            "total_engagement": row.total_engagement or 0
        }
        for row in source_stats
    ]

    return {
        "total_mentions": total_mentions,
        "total_engagement": total_engagement,
        "by_source": by_source
    }