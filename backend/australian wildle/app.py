# ---------- Imports ----------
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import csv
import os
import hmac
import hashlib
import pytz
import datetime as dt

# ---------- Constants ----------
AUS_TZ = pytz.timezone("Australia/Melbourne")
CSV_PATH = os.environ.get("WILDLE_CSV", "animal_details_top_animals_pruned.csv")
SECRET = os.environ.get("WILDLE_SECRET", "change-me-please")

EPBC_ORDER = ["Present", "Vulnerable", "Endangered", "Critically Endangered"]
SIZE_ORDER = ["Small", "Medium", "Large", "Very Large"]
EPBC_RANK = {v: i for i, v in enumerate(EPBC_ORDER)}
SIZE_RANK = {v: i for i, v in enumerate(SIZE_ORDER)}

# ---------- App ----------
app = FastAPI()

# ---------- Data models ----------
class GuessIn(BaseModel):
    guess_name: str

# ---------- Load data ----------
def _load_rows(path: str) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def _derive_diet(row: Dict[str, Any]) -> List[str]:
    items = set()
    for k, v in row.items():
        if k.startswith("top_diet_") and str(v).strip().lower() in ("true", "1"):
            items.add(k.replace("top_diet_", ""))
        if k.startswith("eats_") and str(v).strip().lower() in ("true", "1"):
            items.add(k.replace("eats_", ""))
    return sorted(items)

def _derive_habitats(row: Dict[str, Any]) -> List[str]:
    v = (row.get("foraging_top") or "").strip()
    return [v] if v else []

_SPECIES_ROWS: List[Dict[str, Any]] = _load_rows(CSV_PATH)
# normalise keys used later
for r in _SPECIES_ROWS:
    r["CommonName"] = r.get("CommonName") or r.get("common_name") or ""
    r["ScientificName"] = r.get("ScientificName") or r.get("scientific_name") or ""
# stable order so the same hash maps to the same species even if CSV order changes
_SPECIES_ROWS.sort(key=lambda r: (r.get("ScientificName",""), r.get("CommonName","")))
# precompute derived fields
for r in _SPECIES_ROWS:
    r["diet"] = _derive_diet(r)
    r["habitats"] = _derive_habitats(r)

# ---------- Daily selection (deterministic) ----------
def _today_au(now_utc: Optional[dt.datetime] = None) -> dt.datetime:
    now_utc = now_utc or dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
    return now_utc.astimezone(AUS_TZ)

def _game_date_str() -> str:
    return _today_au().strftime("%Y-%m-%d")

def _seconds_until_reset() -> int:
    now = _today_au()
    tomorrow = (now + dt.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return max(0, int((tomorrow - now).total_seconds()))

def _pick_daily_index(secret: str, date_str: str, n: int) -> int:
    mac = hmac.new(secret.encode(), date_str.encode(), hashlib.sha256).digest()
    return int.from_bytes(mac[:8], "big") % max(1, n)

def _daily_target() -> Dict[str, Any]:
    if not _SPECIES_ROWS:
        raise HTTPException(500, "no species loaded")
    idx = _pick_daily_index(SECRET, _game_date_str(), len(_SPECIES_ROWS))
    return _SPECIES_ROWS[idx]

def _opaque_id(row: Dict[str, Any], date_str: str) -> str:
    key = f"{date_str}|{row.get('ScientificName','')}"
    return hmac.new(SECRET.encode(), key.encode(), hashlib.sha256).hexdigest()[:16]

# ---------- Feedback helpers ----------
def _enum_hint_value(guess: Optional[str], target: Optional[str]) -> Dict[str, Any]:
    if guess == target:
        return {"state": "correct", "guess": guess}
    if guess is None:
        return {"state": "unknown", "guess": None}
    return {"state": "incorrect", "guess": guess}

def _ordered_hint_value(guess: Optional[str], target: Optional[str], rank: Dict[str, int]) -> Dict[str, Any]:
    if guess == target:
        return {"state": "correct", "guess": guess}
    if guess not in rank or target not in rank:
        return {"state": "unknown", "guess": guess}
    return {
        "state": "partial",
        "guess": guess,
        "direction": "higher" if rank[guess] > rank[target] else "lower",
    }

def _list_hint_value(guess_list: Optional[List[str]], target_list: Optional[List[str]]) -> Dict[str, Any]:
    gs, ts = list(guess_list or []), list(target_list or [])
    gset, tset = set(gs), set(ts)
    if gset == tset:
        return {"state": "correct", "guess": gs}
    overlap = sorted(gset & tset)
    if overlap:
        return {"state": "partial", "guess": gs, "overlap": overlap}
    return {"state": "incorrect", "guess": gs}

def _with_target_value(token: Dict[str, Any], target_value: Any, reveal: bool) -> Dict[str, Any]:
    # Attach the target’s value only when reveal=True (e.g., solved). Keeps gameplay spoiler-free otherwise.
    if reveal:
        enriched = dict(token)
        enriched["target"] = target_value
        return enriched
    return token

def _by_common_name() -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for r in _SPECIES_ROWS:
        name = (r.get("CommonName") or "").strip()
        if name:
            out[name.lower()] = r
    return out

def _make_feedback(guess_row: Dict[str, Any], target_row: Dict[str, Any], reveal: bool) -> Dict[str, Any]:
    # Build Narutodle-style tokens with the guessed entries shown, plus target entries when reveal=True.
    f: Dict[str, Any] = {}
    f["taxon_class_ET"] = _with_target_value(
        _enum_hint_value(guess_row.get("taxon_class_ET"), target_row.get("taxon_class_ET")),
        target_row.get("taxon_class_ET"),
        reveal,
    )
    f["EPBCThreatStatus"] = _with_target_value(
        _ordered_hint_value(guess_row.get("EPBCThreatStatus"), target_row.get("EPBCThreatStatus"), EPBC_RANK),
        target_row.get("EPBCThreatStatus"),
        reveal,
    )
    f["size_bucket"] = _with_target_value(
        _ordered_hint_value(guess_row.get("size_bucket"), target_row.get("size_bucket"), SIZE_RANK),
        target_row.get("size_bucket"),
        reveal,
    )
    f["activity_top"] = _with_target_value(
        _enum_hint_value(guess_row.get("activity_top"), target_row.get("activity_top")),
        target_row.get("activity_top"),
        reveal,
    )
    f["habitats"] = _with_target_value(
        _list_hint_value(guess_row.get("habitats"), target_row.get("habitats")),
        target_row.get("habitats"),
        reveal,
    )
    f["diet"] = _with_target_value(
        _list_hint_value(guess_row.get("diet"), target_row.get("diet")),
        target_row.get("diet"),
        reveal,
    )
    return f

# ---------- Routes ----------
@app.get("/wildle/today")
def game_today():
    date_str = _game_date_str()
    target = _daily_target()
    return {
        "game_date": date_str,
        "seconds_until_reset": _seconds_until_reset(),
        "animal_id": _opaque_id(target, date_str),
        "display_fields": [
            {"key": "taxon_class_ET", "type": "enum", "label": "Class"},
            {"key": "EPBCThreatStatus", "type": "ordered", "label": "EPBC Status", "order": EPBC_ORDER},
            {"key": "size_bucket", "type": "ordered", "label": "Size", "order": SIZE_ORDER},
            {"key": "activity_top", "type": "enum", "label": "Activity"},
            {"key": "habitats", "type": "list", "label": "Habitats"},
            {"key": "diet", "type": "list", "label": "Diet"},
        ],
        "vocab": {
            "animals": [r["CommonName"] for r in _SPECIES_ROWS if r.get("CommonName")]
        },
    }

@app.post("/wildle/guess")
def game_guess(payload: GuessIn):
    name = payload.guess_name.strip().lower()
    by_name = _by_common_name()
    guess_row = by_name.get(name)
    if not guess_row:
        raise HTTPException(404, "unknown animal name")

    target = _daily_target()
    solved = (guess_row.get("CommonName") == target.get("CommonName"))

    # Add guessed snapshot so the client can render chips/labels alongside the tokens
    guess_snapshot = {
        "CommonName": guess_row.get("CommonName"),
        "taxon_class_ET": guess_row.get("taxon_class_ET"),
        "EPBCThreatStatus": guess_row.get("EPBCThreatStatus"),
        "size_bucket": guess_row.get("size_bucket"),
        "activity_top": guess_row.get("activity_top"),
        "habitats": guess_row.get("habitats"),
        "diet": guess_row.get("diet"),
    }

    feedback = _make_feedback(guess_row, target, reveal=solved)

    return {
        "game_date": _game_date_str(),
        "solved": solved,
        "guess": guess_snapshot,
        "feedback": feedback
    }

@app.get("/wildle/history")
def game_history(limit: int = 30):
    out: List[Dict[str, Any]] = []
    n = len(_SPECIES_ROWS)
    if n == 0:
        return out
    now = _today_au()
    for i in range(max(0, limit)):
        date = now - dt.timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        idx = _pick_daily_index(SECRET, date_str, n)
        row = _SPECIES_ROWS[idx]
        out.append({
            "date": date_str,
            "animal_id": _opaque_id(row, date_str),
            "reveal_name": row.get("CommonName"),
        })
    return out
