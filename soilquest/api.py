"""Bounded loopback API. No flight controls or real chemical measurements."""
from pathlib import Path
from fastapi import FastAPI,HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .simulation import run
ROOT=Path(__file__).resolve().parents[1]
app=FastAPI(title='SoilQuest AI',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://127.0.0.1:5104'],allow_methods=['GET'])
@app.get('/api/health')
def health():return {'ok':True,'synthetic':True}
@app.get('/api/survey')
def survey(seed:int=Query(41,ge=0,le=100000),family:str='narrow',policy:str='balanced',budget:int=Query(20,ge=1,le=40),travel:float=Query(650,ge=0,le=2000)):
 try:return run(seed,family,policy,budget,travel)
 except ValueError as exc:raise HTTPException(400,str(exc)) from exc
if (ROOT/'frontend/dist').exists():app.mount('/',StaticFiles(directory=ROOT/'frontend/dist',html=True),name='frontend')
