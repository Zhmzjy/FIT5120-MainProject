from flask import Blueprint, request, jsonify
import csv
import math
import uuid
import os
from typing import Dict, List, Optional

ai_challenge_bp = Blueprint('ai_challenge', __name__)

class Species:
    def __init__(self, id: str, common_name: str, scientific_name: str, attrs: Dict[str, Optional[bool]]):
        self.id = id
        self.common_name = common_name
        self.scientific_name = scientific_name
        self.attrs = attrs

class Question:
    def __init__(self, id: str, text: str, attribute: str, qtype: str = "boolean"):
        self.id = id
        self.text = text
        self.attribute = attribute
        self.qtype = qtype

class SessionState:
    def __init__(self):
        self.candidates = {}
        self.asked = []
        self.answers = {}

SPECIES: List[Species] = []
QUESTIONS: List[Question] = []
SESSIONS: Dict[str, SessionState] = {}

P_YES_TRUE = 0.95
P_YES_FALSE = 0.05
P_NO_TRUE = 0.05
P_NO_FALSE = 0.95
P_DONT_KNOW = 0.90

EXPLORE_QUESTIONS = 5
EXPLOIT_CONF_THRESHOLD = 0.75
YES_BONUS_WEIGHT = 0.25
TOPK_FOR_YES_BONUS = 3
CONFIDENCE_THRESHOLD = 0.70
MAX_QUESTIONS = 20

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
    out = []
    raw_rows = []
    for i, row in enumerate(rows):
        sid = row.get("id") or f"s{i+1:03d}"
        species = Species(
            id=sid,
            common_name=row.get("CommonName") or row.get("common_name") or "",
            scientific_name=row.get("ScientificName") or row.get("scientific_name") or "",
            attrs={}
        )
        out.append(species)
        raw_rows.append(row)
    return out, raw_rows

def load_bool_questions(path: str) -> List[Question]:
    rows = _load_rows(path)
    qlist = []
    seen = set()
    for r in rows:
        field = (r.get("Field") or "").strip()
        text = (r.get("Question") or "").strip()
        if not field or not text or field in seen:
            continue
        seen.add(field)
        qlist.append(Question(
        if not USE_IBRA_QUESTIONS and field.lower().startswith("ibra_"):
            continue
            id=f"q_{field}",
            text=text,
            attribute=field,
            qtype="boolean"
        ))
    return qlist

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

    neww = {}
    for sid, w in weights.items():
        sp = get_species_by_id(sid)
        val = sp.attrs.get(q.attribute)

        if ans == "yes":
            if val is True:
                w *= P_YES_TRUE
            else:
                w *= P_YES_FALSE
        else:
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

    _, best_conf = best_guess(state)
    hone_in = (len(state.asked) >= EXPLORE_QUESTIONS) or (best_conf >= EXPLOIT_CONF_THRESHOLD)

    topk = _topk_by_weight(state, TOPK_FOR_YES_BONUS)
    topk_total = sum(w for _, w in topk) or 1.0

    best_q, best_score = None, -1e18

    for q in QUESTIONS:
        if q.id in asked:
            continue

        exp_h = 0.0
        priors = [0.45, 0.45, 0.10]
        for p_out, out in zip(priors, ["yes", "no", "dont_know"]):
            nxt = simulate_update(cur_w, q, out)
            exp_h += p_out * entropy(nxt)
        gain = cur_h - exp_h

        if hone_in:
            yes_mass = 0.0
            for sid, w in topk:
                sp = get_species_by_id(sid)
                val = sp.attrs.get(q.attribute)
                if val is True:
                    yes_mass += w
            p_yes_topk = yes_mass / topk_total

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

def init_ai_challenge():
    global SPECIES, QUESTIONS

    base_dir = os.path.dirname(os.path.dirname(__file__))
    details_csv = os.path.join(base_dir, "ai classifier challenge", "animal_details_top_animals.csv")
    bool_q_csv = os.path.join(base_dir, "ai classifier challenge", "dictionary_questions_bool.csv")

    SPECIES, raw_rows = load_species(details_csv)
    QUESTIONS = load_bool_questions(bool_q_csv)

    bool_fields = [q.attribute for q in QUESTIONS]
    for sp, raw in zip(SPECIES, raw_rows):
        attrs = {}
        for f in bool_fields:
            attrs[f] = _as_bool(raw.get(f))
        sp.attrs = attrs

    for species in SPECIES:
        for session_id in SESSIONS:
            SESSIONS[session_id].candidates[species.id] = 1.0

@ai_challenge_bp.route('/session/new', methods=['POST'])
def new_session():
    sid = str(uuid.uuid4())
    state = SessionState()
    state.candidates = {s.id: 1.0 for s in SPECIES}
    SESSIONS[sid] = state
    return jsonify({"session_id": sid})

@ai_challenge_bp.route('/next_question', methods=['GET'])
def next_question():
    session_id = request.args.get('session_id')
    if not session_id or session_id not in SESSIONS:
        return jsonify({"error": "unknown session"}), 404

    st = SESSIONS[session_id]

    if should_decide(st):
        return jsonify({"decision": decision_payload(st)})

    q = select_next_question(st)
    if not q:
        return jsonify({"decision": decision_payload(st)})

    return jsonify({
        "question": {
            "id": q.id,
            "text": q.text,
            "attribute": q.attribute,
            "qtype": q.qtype
        }
    })

@ai_challenge_bp.route('/answer', methods=['POST'])
def answer():
    data = request.get_json()
    session_id = data.get('session_id')
    question_id = data.get('question_id')
    answer_text = data.get('answer')

    if not session_id or session_id not in SESSIONS:
        return jsonify({"error": "unknown session"}), 404

    st = SESSIONS[session_id]

    q = next((qq for qq in QUESTIONS if qq.id == question_id), None)
    if not q:
        return jsonify({"error": "unknown question"}), 404

    ans = answer_text.strip().lower()
    if ans not in ("yes","no","dont_know"):
        return jsonify({"error": "answer must be yes/no/dont_know"}), 400

    apply_answer(st, q, ans)

    if should_decide(st):
        return jsonify({"decision": decision_payload(st)})

    nxt = select_next_question(st)
    if not nxt:
        return jsonify({"decision": decision_payload(st)})

    sid, conf = best_guess(st)
    sp = get_species_by_id(sid)
    return jsonify({
        "next_question": {
            "id": nxt.id,
            "text": nxt.text,
            "attribute": nxt.attribute,
            "qtype": nxt.qtype
        },
        "top_guess_preview": {
            "id": sp.id,
            "common_name": sp.common_name,
            "scientific_name": sp.scientific_name,
            "confidence": round(conf, 3),
        },
    })

@ai_challenge_bp.route('/guess', methods=['GET'])
def guess():
    session_id = request.args.get('session_id')
    if not session_id or session_id not in SESSIONS:
        return jsonify({"error": "unknown session"}), 404

    st = SESSIONS[session_id]
    sid, conf = best_guess(st)
    sp = get_species_by_id(sid)
    return jsonify({
        "id": sp.id,
        "common_name": sp.common_name,
        "scientific_name": sp.scientific_name,
        "confidence": round(conf, 3),
    })

@ai_challenge_bp.route('/reset', methods=['POST'])
def reset():
    data = request.get_json()
    session_id = data.get('session_id')

    if not session_id or session_id not in SESSIONS:
        return jsonify({"error": "unknown session"}), 404

    state = SessionState()
    state.candidates = {s.id: 1.0 for s in SPECIES}
    SESSIONS[session_id] = state
    return jsonify({"ok": True})
