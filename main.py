import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from schemas import ContactMessage
from database import create_document, db

app = FastAPI(title="Abdulrahman Sakah Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Portfolio API running"}

@app.get("/api/profile")
def profile() -> Dict[str, Any]:
    return {
        "name": "Abdulrahman Sakah",
        "title": "Full‑Stack Developer",
        "location": "Karlskrona, Sweden",
        "summary": (
            "Creative full‑stack engineer crafting immersive web experiences. "
            "Multiple years building scalable backends and delightful frontends."
        ),
        "skills": [
            "TypeScript", "React", "Next.js", "Node.js", "Python", "FastAPI", "GraphQL",
            "MongoDB", "PostgreSQL", "Docker", "CI/CD", "AWS", "Tailwind CSS"
        ],
        "links": {
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "email": "mailto:contact@sakah.dev"
        }
    }

@app.post("/api/contact")
def submit_contact(payload: ContactMessage):
    try:
        doc_id = create_document("contactmessage", payload)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
