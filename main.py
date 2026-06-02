from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Setup Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Depoimento(BaseModel):
    data_hora: datetime
    nome: str
    texto: str
    nota: int
    nicho: str

@app.post("/depoimentos")
async def criar_depoimento(depoimento: Depoimento):
    try:
        # Convert datetime to ISO string for Supabase
        depoimento_dict = depoimento.model_dump()
        depoimento_dict['data_hora'] = depoimento_dict['data_hora'].isoformat()
        
        response = supabase.table("depoimentos").insert(depoimento_dict).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/depoimentos")
async def listar_depoimentos():
    try:
        response = supabase.table("depoimentos").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run("main:app", host="0.0.0.0", port=port)
