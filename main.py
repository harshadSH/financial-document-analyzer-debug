from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment, verification

# DB
from database import SessionLocal
from models import Analysis


app = FastAPI(title="Financial Document Analyzer")


# Run Crew
def run_crew(query: str, file_path: str):
    crew = Crew(
        agents=[financial_analyst, verifier, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff(
        inputs={
            "query": query,
            "file_path": file_path
        }
    )

    return result


# Background Task Function
def process_document(file_path: str, query: str):
    try:
        result = run_crew(query=query, file_path=file_path)

        db = SessionLocal()

        record = Analysis(
            query=query,
            result=str(result),
            file_name=file_path
        )

        db.add(record)
        db.commit()
        db.close()

    except Exception as e:
        print("Background Task Error:", str(e))

    finally:
        # Cleanup file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


# Health Check
@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


# Analyze API (ASYNC)
@app.post("/analyze")
async def analyze_api(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        if not query:
            query = "Analyze this financial document"

        # 🔥 Run in background
        background_tasks.add_task(process_document, file_path, query.strip())

        return {
            "status": "processing",
            "message": "Your document is being analyzed in the background"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}"
        )


# Get History (DB)
@app.get("/history")
def get_history():
    db = SessionLocal()
    records = db.query(Analysis).all()
    db.close()

    return [
        {
            "id": r.id,
            "query": r.query,
            "result": r.result,
            "file_name": r.file_name
        }
        for r in records
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)