from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from src.pipeline import RAGPipeline
import time
import uvicorn

app = FastAPI(title="BIS Standards API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline with LLM enabled for "perfect" query output
pipeline = RAGPipeline(use_llm_expansion=True)

@app.get("/search")
async def search(
    query: str = Query(..., min_length=1),
    lang: str = Query("en", regex="^(en|hi|te)$")
):
    start_time = time.perf_counter()
    
    # Run the pipeline with the specified language
    results_data, chunks = pipeline.run_with_details(query, k=5, lang=lang)
    
    latency = round(time.perf_counter() - start_time, 2)
    
    # Format results for the frontend
    results = []
    for item in results_data:
        std_id = item.get("standard_id", "Unknown")
        
        results.append({
            "id": std_id,
            "title": item.get("title", f"Standard {std_id}"),
            "category": "Technical Standard",
            "confidenceScore": 95 if item.get("rationale") else 80,
            "summary": item.get("summary", "No summary available."),
            "rationale": item.get("rationale", "No rationale generated."),
            "entities": [], # Could be extracted by LLM in future
            "stats": [
                {"name": "Jan", "value": 400},
                {"name": "Feb", "value": 300},
                {"name": "Mar", "value": 600},
                {"name": "Apr", "value": 800},
            ]
        })
        
    return {
        "query": query,
        "results": results,
        "latency": latency,
        "lang": lang
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
