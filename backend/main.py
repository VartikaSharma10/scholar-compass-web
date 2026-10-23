import json
from pathlib import Path
from typing import List, Literal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Scholar Compass API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATA = json.loads((Path(__file__).parent / "scholarships.json").read_text(encoding="utf-8"))


class Profile(BaseModel):
    cgpa: float = Field(ge=0)
    scale: Literal[4, 10] = 10
    english_done: bool = False
    research: Literal["none", "proj", "pub"] = "proj"
    countries: List[str] = []
    needs: List[Literal["tuition", "stipend"]] = []


def score(o: dict, p: Profile, g: float):
    s, why, check = 50, [], []
    if g >= o["min_gpa"] + 0.5:
        s += 20; why.append("CGPA comfortably above the typical bar")
    elif g >= o["min_gpa"]:
        s += 10; why.append("CGPA meets the typical bar")
    else:
        s -= 15; check.append("CGPA may be below the usual range here, check programme minimums")
    if o["needs_english"]:
        if p.english_done: s += 10
        else: s -= 5; check.append("English test (IELTS/TOEFL) needed, book it early")
    rl = {"none": 0, "proj": 1, "pub": 2}[p.research]
    if o["research_level"] >= 2 and rl < 2:
        s -= 15; check.append("Expects strong research output, a paper would help")
    elif o["research_level"] == 1 and rl >= 1:
        s += 10; why.append("Your projects support a research pitch")
    elif o["research_level"] == 1:
        s -= 5; check.append("Needs some research evidence")
    if "tuition" in p.needs and o["tuition"]: s += 5
    if "stipend" in p.needs and o["stipend"]: s += 5
    if "stipend" in p.needs and not o["stipend"]:
        check.append("Does not cover living costs on its own")
    return max(5, min(98, s)), why, check


@app.get("/api/health")
def health():
    return {"status": "ok", "count": len(DATA)}


@app.get("/api/scholarships")
def list_all():
    return DATA


@app.post("/api/match")
def match(p: Profile):
    g = p.cgpa * 2.5 if p.scale == 4 else p.cgpa
    out = []
    for o in DATA:
        if p.countries and o["country"] not in p.countries:
            continue
        s, why, check = score(o, p, g)
        out.append({**o, "score": s, "why": why, "check": check})
    return sorted(out, key=lambda x: x["score"], reverse=True)
