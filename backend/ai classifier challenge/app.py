# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import csv
import math
import uuid

app = FastAPI()

# ---------- Data models ----------

class Species(BaseModel):
    id: str
    common_name: str
    scientific_name: str
    attrs: Dict[str, object]  # bool/None

class Question(BaseModel):
    id: str
    text: str
    attribute: str  # e.g., "omnivore_flag"
    qtype: str      # "boolean"

class AnswerPayload(BaseModel):
    session_id: str
    question_id: str
    answer: str  # "yes" | "no" | "dont_know"

# ---------- Load data ----------

DETAILS_CSV = "animal_details_top_animals.csv"
BOOL_Q_CSV  = "dictionary_questions_bool.csv"

SPECIES: List[Species] = []
QUESTIONS: List[Question] = []

def _as_bool(v: Optional[str]) -> Optional[bool]:
    if v is None:
        return None
    s = str(v).strip().lower()
    if s in ("1","true","yes","y","t"):
        return True
    if s in ("0","false","no","n","f"):
        return False
    return None

def _load_rows(path: str) -> List[Dict[str,str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_species(path: str) -> List[Species]:
    rows = _load_rows(path)
    out: List[Species] = []
    for i, row in enumerate(rows):
        sid = row.get("id") or f"s{i+1:03d}"
        out.append(Species(
            id=sid,
            common_name=row.get("CommonName") or row.get("common_name") or "",
            scientific_name=row.get("ScientificName") or row.get("scientific_name") or "",
            attrs={},  # filled after we know which fields are in bool.csv
        ))
    return out, rows

USE_IBRA_QUESTIONS = False # whether to include IBRA-related questions

def load_bool_questions(path: str) -> List[Question]:
    rows = _load_rows(path)
    qlist: List[Question] = []
    seen = set()
    for r in rows:
        field = (r.get("Field") or "").strip()
        text  = (r.get("Question") or "").strip()
        if not field or not text or field in seen:
            continue
        if not USE_IBRA_QUESTIONS and field.lower().startswith("ibra_"):
            continue
        seen.add(field)
        qlist.append(Question(
            id=f"q_{field}",
            text=text,
            attribute=field,
            qtype="boolean",
        ))
    return qlist


# initialise species + raw rows
SPECIES, _SPECIES_ROWS = load_species(DETAILS_CSV)
# initialise questions (authoritative list of boolean fields)
QUESTIONS = load_bool_questions(BOOL_Q_CSV)

# project the boolean attributes for each species strictly to fields in bool.csv
BOOL_FIELDS = [q.attribute for q in QUESTIONS]
for sp, raw in zip(SPECIES, _SPECIES_ROWS):
    attrs: Dict[str, object] = {}
    for f in BOOL_FIELDS:
        attrs[f] = _as_bool(raw.get(f))
    sp.attrs = attrs

# ---------- Sessions & inference ----------

class SessionState:
    def __init__(self):
        self.candidates = {s.id: 1.0 for s in SPECIES}
        self.asked: List[str] = []
        self.answers: Dict[str, str] = {}  # qid -> "yes"/"no"/"dont_know"

SESSIONS: Dict[str, SessionState] = {}

P_YES_TRUE     = 0.95
P_YES_FALSE    = 0.05
P_NO_TRUE      = 0.05
P_NO_FALSE     = 0.95
P_DONT_KNOW    = 0.90

# Exploration to Exploitation schedule
EXPLORE_QUESTIONS      = 5     # stay neutral (pure info gain) for the first N questions
EXPLOIT_CONF_THRESHOLD = 0.75  # or when best guess confidence passes this, start honing in
YES_BONUS_WEIGHT       = 0.25  # how much to favour questions likely to get a "yes" in hone-in phase
TOPK_FOR_YES_BONUS     = 3     # look at the top-K candidates to estimate yes-likelihood

CONFIDENCE_THRESHOLD = 0.70
MAX_QUESTIONS = 20

def normalize(weights: Dict[str, float]) -> Dict[str, float]:
    tot = sum(weights.values())
    if tot <= 0:
        n = len(weights)
        return {k: 1.0/n for k in weights} if n else {}
    return {k: v/tot for k,v in weights.items()}

def entropy(weights: Dict[str, float]) -> float:
    tot = sum(weights.values())
    h = 0.0
    for v in weights.values():
        p = v / tot if tot else 0.0
        if p > 0:
            h -= p * math.log2(p)
    return h

def get_species_by_id(sid: str) -> Species:
    for s in SPECIES:
        if s.id == sid:
            return s
    raise KeyError(sid)

def best_guess(state: SessionState):
    w = normalize(state.candidates)
    sid, val = max(w.items(), key=lambda kv: kv[1])
    return sid, val

def decision_payload(state: SessionState):
    sid, conf = best_guess(state)
    sp = get_species_by_id(sid)
    reason = (
        "confidence_threshold" if conf >= CONFIDENCE_THRESHOLD
        else ("max_questions" if len(state.asked) >= MAX_QUESTIONS else "no_questions_left")
    )
    return {
        "id": sp.id,
        "common_name": sp.common_name,
        "scientific_name": sp.scientific_name,
        "confidence": round(conf, 3),
        "reason": reason,
        "questions_asked": len(state.asked),
    }

def should_decide(state: SessionState) -> bool:
    sid, conf = best_guess(state)
    if conf >= CONFIDENCE_THRESHOLD:
        return True
    if len(state.asked) >= MAX_QUESTIONS:
        return True
    remaining = [q for q in QUESTIONS if q.id not in state.asked]
    return not remaining

def simulate_update(weights: Dict[str, float], q: Question, ans: str) -> Dict[str, float]:
    if ans == "dont_know":
        return normalize(dict(weights))

    neww: Dict[str, float] = {}
    for sid, w in weights.items():
        sp = get_species_by_id(sid)
        val = sp.attrs.get(q.attribute)  # True / False (dataset is boolean)

        if ans == "yes":
            if val is True:
                w *= P_YES_TRUE
            else:  # val is False (or absent, treated as neutral)
                w *= P_YES_FALSE
        else:  # ans == "no"
            if val is True:
                w *= P_NO_TRUE
            else:
                w *= P_NO_FALSE

        neww[sid] = w

    return normalize(neww)


def _topk_by_weight(state: SessionState, k: int):
    w = normalize(state.candidates)
    return sorted(w.items(), key=lambda kv: kv[1], reverse=True)[:max(1, k)]


def select_next_question(state: SessionState) -> Question:
    asked = set(state.asked)
    cur_w = normalize(state.candidates)
    cur_h = entropy(cur_w)

    # decide whether to hone in yet
    _, best_conf = best_guess(state)
    hone_in = (len(state.asked) >= EXPLORE_QUESTIONS) or (best_conf >= EXPLOIT_CONF_THRESHOLD)

    # cache top-k for yes-bias
    topk = _topk_by_weight(state, TOPK_FOR_YES_BONUS)
    topk_total = sum(w for _, w in topk) or 1.0

    best_q, best_score = None, -1e18

    for q in QUESTIONS:
        if q.id in asked:
            continue

        # --- base: expected information gain (symmetric yes/no/dont_know priors) ---
        exp_h = 0.0
        priors = [0.45, 0.45, 0.10]  # yes / no / dont_know
        for p_out, out in zip(priors, ["yes", "no", "dont_know"]):
            nxt = simulate_update(cur_w, q, out)
            exp_h += p_out * entropy(nxt)
        gain = cur_h - exp_h

        # --- hone-in bonus: favour questions top-k are likely to answer "yes" to ---
        if hone_in:
            # estimate P(answer=="yes" | top-k)
            # treat missing as False for this heuristic (dataset is boolean in your case)
            yes_mass = 0.0
            for sid, w in topk:
                sp = get_species_by_id(sid)
                val = sp.attrs.get(q.attribute)  # True/False
                if val is True:
                    yes_mass += w
            p_yes_topk = yes_mass / topk_total  # 0..1

            # blend info gain with yes-likelihood
            score = gain * (1.0 - YES_BONUS_WEIGHT) + YES_BONUS_WEIGHT * p_yes_topk
        else:
            score = gain

        if score > best_score:
            best_score = score
            best_q = q

    return best_q


def apply_answer(state: SessionState, q: Question, ans: str):
    state.asked.append(q.id)
    state.answers[q.id] = ans
    state.candidates = simulate_update(state.candidates, q, ans)

# ---------- Routes ----------

@app.post("/session/new")
def new_session():
    sid = str(uuid.uuid4())
    SESSIONS[sid] = SessionState()
    return {"session_id": sid}

@app.get("/next_question")
def next_question(session_id: str):
    st = SESSIONS.get(session_id)
    if not st:
        raise HTTPException(404, "unknown session")

    if should_decide(st):
        return {"decision": decision_payload(st)}

    q = select_next_question(st)
    if not q:
        return {"decision": decision_payload(st)}

    # keep shape consistent with existing client
    return {"question": q.dict()}

@app.post("/answer")
def answer(payload: AnswerPayload):
    st = SESSIONS.get(payload.session_id)
    if not st:
        raise HTTPException(404, "unknown session")

    q = next((qq for qq in QUESTIONS if qq.id == payload.question_id), None)
    if not q:
        raise HTTPException(404, "unknown question")

    ans = payload.answer.strip().lower()
    if ans not in ("yes","no","dont_know"):
        raise HTTPException(400, "answer must be yes/no/dont_know")

    apply_answer(st, q, ans)

    if should_decide(st):
        return {"decision": decision_payload(st)}

    nxt = select_next_question(st)
    if not nxt:
        return {"decision": decision_payload(st)}

    sid, conf = best_guess(st)
    sp = get_species_by_id(sid)
    return {
        "next_question": nxt.dict(),
        "top_guess_preview": {
            "id": sp.id,
            "common_name": sp.common_name,
            "scientific_name": sp.scientific_name,
            "confidence": round(conf, 3),
        },
    }

@app.get("/guess")
def guess(session_id: str):
    st = SESSIONS.get(session_id)
    if not st:
        raise HTTPException(404, "unknown session")
    sid, conf = best_guess(st)
    sp = get_species_by_id(sid)
    return {
        "id": sp.id,
        "common_name": sp.common_name,
        "scientific_name": sp.scientific_name,
        "confidence": round(conf, 3),
    }

@app.post("/reset")
def reset(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(404, "unknown session")
    SESSIONS[session_id] = SessionState()
    return {"ok": True}
