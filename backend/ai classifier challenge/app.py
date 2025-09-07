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
    attrs: Dict[str, object]  # bool/str


class Question(BaseModel):
    id: str
    text: str
    attribute: str  # e.g., "has_feathers"
    qtype: str  # "boolean" or "enum"


class AnswerPayload(BaseModel):
    session_id: str
    question_id: str
    answer: str  # "yes" | "no" | "unsure" (or enum value)


# ---------- Load species CSV ----------

ATTR_COLS = [
    "is_mammal",
    "is_bird",
    "is_reptile",
    "is_amphibian",
    "is_fish",
    "is_invertebrate",
    "lays_eggs",
    "is_marsupial",
    "is_monotreme",
    "can_fly",
    "can_glide",
    "is_venomous",
    "is_marine",
    "is_freshwater",
    "is_terrestrial",
    "is_nocturnal",
    "is_diurnal",
    "is_arboreal",
    "is_burrowing",
    "is_endemic",
    "has_pouch",
    "has_shell_or_spines",
    "has_feathers",
    "has_scales",
    "has_fur",
    "diet",
    "primary_habitat",
    "locomotion",
    "size_band",
    "conservation",
    "region_hint",
]

SPECIES: List[Species] = []


def _as_bool(v: str) -> Optional[bool]:
    if v in ("1", "true", "True", "yes", "Yes"):
        return True
    if v in ("0", "false", "False", "no", "No"):
        return False
    return None


def load_species_csv(path="species.csv"):
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            attrs = {}
            for k in ATTR_COLS:
                if k in (
                    "diet",
                    "primary_habitat",
                    "locomotion",
                    "size_band",
                    "conservation",
                    "region_hint",
                ):
                    attrs[k] = row[k].strip() if row[k] else None
                else:
                    attrs[k] = _as_bool(row[k])
            out.append(
                Species(
                    id=row["id"],
                    common_name=row["common_name"],
                    scientific_name=row["scientific_name"],
                    attrs=attrs,
                )
            )
    return out


SPECIES = load_species_csv()

# ---------- Questions (map 1:1 to attributes) ----------

QUESTIONS: List[Question] = [
    Question(
        id="q_feathers",
        text="Does it have feathers?",
        attribute="has_feathers",
        qtype="boolean",
    ),
    Question(
        id="q_scales",
        text="Does it have scales?",
        attribute="has_scales",
        qtype="boolean",
    ),
    Question(
        id="q_fur", text="Does it have fur?", attribute="has_fur", qtype="boolean"
    ),
    Question(
        id="q_lays_eggs",
        text="Does it lay eggs?",
        attribute="lays_eggs",
        qtype="boolean",
    ),
    Question(
        id="q_pouch",
        text="Does it have a pouch (marsupial)?",
        attribute="is_marsupial",
        qtype="boolean",
    ),
    Question(
        id="q_monotreme",
        text="Is it a monotreme (platypus/echidna)?",
        attribute="is_monotreme",
        qtype="boolean",
    ),
    Question(id="q_fly", text="Can it fly?", attribute="can_fly", qtype="boolean"),
    Question(
        id="q_glide", text="Can it glide?", attribute="can_glide", qtype="boolean"
    ),
    Question(
        id="q_venom", text="Is it venomous?", attribute="is_venomous", qtype="boolean"
    ),
    Question(
        id="q_marine",
        text="Do you mostly find it in the ocean?",
        attribute="is_marine",
        qtype="boolean",
    ),
    Question(
        id="q_fresh",
        text="Do you find it in rivers or lakes?",
        attribute="is_freshwater",
        qtype="boolean",
    ),
    Question(
        id="q_arboreal",
        text="Does it live in trees a lot?",
        attribute="is_arboreal",
        qtype="boolean",
    ),
    Question(
        id="q_burrow",
        text="Does it dig or live in burrows?",
        attribute="is_burrowing",
        qtype="boolean",
    ),
    Question(
        id="q_nocturnal",
        text="Is it mostly active at night?",
        attribute="is_nocturnal",
        qtype="boolean",
    ),
    Question(
        id="q_diurnal",
        text="Is it mostly active in the day?",
        attribute="is_diurnal",
        qtype="boolean",
    ),
    Question(
        id="q_locomotion_slither",
        text="Does it slither?",
        attribute="locomotion",
        qtype="enum",
    ),
    Question(
        id="q_locomotion_hop", text="Does it hop?", attribute="locomotion", qtype="enum"
    ),
    Question(
        id="q_habitat_ocean",
        text="Is its main home the ocean?",
        attribute="primary_habitat",
        qtype="enum",
    ),
    Question(
        id="q_region_tropical",
        text="Is it from tropical parts of Australia?",
        attribute="region_hint",
        qtype="enum",
    ),
]

# ---------- Sessions & inference ----------


class SessionState:
    def __init__(self):
        self.candidates = {s.id: 1.0 for s in SPECIES}
        self.asked: List[str] = []
        self.answers: Dict[str, str] = {}  # qid -> "yes"/"no"/"unsure" or enum value


SESSIONS: Dict[str, SessionState] = {}

# Likelihoods for boolean Q/A (tweakable)
P_YES_TRUE = 0.95
P_YES_FALSE = 0.05
P_NO_TRUE = 0.05
P_NO_FALSE = 0.95
P_UNSURE_DECAY = 0.90

CONFIDENCE_THRESHOLD = 0.70
MAX_QUESTIONS = 20


def decision_payload(state: SessionState):
    sid, conf = best_guess(state)
    sp = get_species_by_id(sid)
    reason = (
        "confidence_threshold"
        if conf >= CONFIDENCE_THRESHOLD
        else (
            "max_questions"
            if len(state.asked) >= MAX_QUESTIONS
            else "no_questions_left"
        )
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
    # stop if any stopping condition is met
    sid, conf = best_guess(state)
    if conf >= CONFIDENCE_THRESHOLD:
        return True
    if len(state.asked) >= MAX_QUESTIONS:
        return True
    # also stop if there are no more questions left to ask
    remaining_questions = [q for q in QUESTIONS if q.id not in state.asked]
    if not remaining_questions:
        return True
    return False


def get_species_by_id(sid: str) -> Species:
    for s in SPECIES:
        if s.id == sid:
            return s
    raise KeyError(sid)


def normalize(weights: Dict[str, float]):
    total = sum(weights.values())
    if total <= 0:
        # reset to uniform if we collapsed accidentally
        n = len(weights)
        return {k: 1.0 / n for k in weights}
    return {k: v / total for k, v in weights.items()}


def entropy(weights: Dict[str, float]) -> float:
    total = sum(weights.values())
    h = 0.0
    for v in weights.values():
        p = v / total if total else 0
        if p > 0:
            h -= p * math.log2(p)
    return h


def simulate_update(
    weights: Dict[str, float], q: Question, hypothetical_answer: str
) -> Dict[str, float]:
    neww = dict(weights)
    for sid in list(neww.keys()):
        sp = get_species_by_id(sid)
        attr_val = sp.attrs.get(q.attribute)
        w = neww[sid]
        if q.qtype == "boolean":
            if hypothetical_answer == "yes":
                if attr_val is True:
                    w *= P_YES_TRUE
                elif attr_val is False:
                    w *= P_YES_FALSE
                else:
                    w *= P_UNSURE_DECAY
            elif hypothetical_answer == "no":
                if attr_val is True:
                    w *= P_NO_TRUE
                elif attr_val is False:
                    w *= P_NO_FALSE
                else:
                    w *= P_UNSURE_DECAY
            else:  # unsure
                w *= P_UNSURE_DECAY
        else:  # enum
            if isinstance(attr_val, str) and hypothetical_answer == attr_val:
                w *= 0.95
            else:
                # soften, don't kill
                w *= 0.75
        neww[sid] = w
    return normalize(neww)


def select_next_question(state: SessionState) -> Question:
    # expected entropy reduction
    best_q, best_gain = None, -1
    current_h = entropy(state.candidates)
    for q in QUESTIONS:
        if q.id in state.asked:
            continue
        outcomes = (
            ["yes", "no", "unsure"]
            if q.qtype == "boolean"
            else [
                "fly",
                "walk",
                "hop",
                "glide",
                "slither",
                "swim",
                "reef",
                "coastal",
                "open_ocean",
                "tropical",
            ]
        )
        # keep outcome set small & relevant; in production, compute from data
        exp_h = 0.0
        # assume naive priors for outcomes
        priors = (
            [0.45, 0.45, 0.10]
            if q.qtype == "boolean"
            else [1 / len(outcomes)] * len(outcomes)
        )
        for p_out, out in zip(priors, outcomes):
            neww = simulate_update(
                state.candidates, q, out if q.qtype == "boolean" else out
            )
            exp_h += p_out * entropy(neww)
        gain = current_h - exp_h
        if gain > best_gain:
            best_gain = gain
            best_q = q
    return best_q


def apply_answer(state: SessionState, q: Question, answer: str):
    state.asked.append(q.id)
    state.answers[q.id] = answer
    state.candidates = simulate_update(state.candidates, q, answer)


def best_guess(state: SessionState):
    weights = normalize(state.candidates)
    sid, w = max(weights.items(), key=lambda kv: kv[1])
    return sid, w


# ---------- Routes ----------


@app.post("/session/new")
def new_session():
    sid = str(uuid.uuid4())
    SESSIONS[sid] = SessionState()
    return {"session_id": sid}


@app.get("/next_question")
def next_question(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(404, "unknown session")
    st = SESSIONS[session_id]

    # If we should stop, return the final decision instead of a question
    if should_decide(st):
        return {"decision": decision_payload(st)}

    q = select_next_question(st)
    if not q:
        # No questions left -> decide anyway
        return {"decision": decision_payload(st)}
    return {"question": q.dict()}


@app.post("/answer")
def answer(payload: AnswerPayload):
    st = SESSIONS.get(payload.session_id)
    if not st:
        raise HTTPException(404, "unknown session")

    q = next((qq for qq in QUESTIONS if qq.id == payload.question_id), None)
    if not q:
        raise HTTPException(404, "unknown question")

    ans = payload.answer.lower()
    if q.qtype == "boolean" and ans not in ("yes", "no", "unsure"):
        raise HTTPException(400, "answer must be yes/no/unsure")

    # Apply the answer update
    apply_answer(st, q, ans)

    # If it’s time to decide, return the decision now
    if should_decide(st):
        return {"decision": decision_payload(st)}

    # Otherwise, return the next question to keep looping
    nxt = select_next_question(st)
    if not nxt:
        # No further questions; decide anyway
        return {"decision": decision_payload(st)}

    # Optional: include a lightweight preview of current top guess (not a decision!)
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
