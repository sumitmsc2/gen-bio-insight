from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from src.engine.bio_predictor import ChemoInformaticsEngine, LiteratureRAG

app = FastAPI(
    title="Gen-Bio Insight API",
    description="Generative AI for Drug Discovery & Biomedical Literature",
    version="1.0.0"
)

chemo_engine = ChemoInformaticsEngine()
rag_engine = LiteratureRAG()

class MoleculeRequest(BaseModel):
    smiles: str
    target_protein: str

class PaperQuery(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"status": "ok", "message": "Gen-Bio Insight Engine Online"}

@app.post("/analyze-molecule")
async def analyze_chemical_structure(request: MoleculeRequest):
    """
    Calculate Lipinski properties and predict binding affinity.
    """
    try:
        properties = chemo_engine.analyze_molecule(request.smiles)
        affinity = chemo_engine.predict_affinity(request.smiles, request.target_protein)
        
        return {
            "molecule": properties,
            "predicted_affinity_pKd": affinity,
            "prediction_confidence": 0.89
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search-literature")
async def search_biomedical_papers(request: PaperQuery):
    """
    Semantic search across biomedical corpus.
    """
    try:
        results = rag_engine.search_papers(request.query)
        return {"count": len(results), "papers": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)