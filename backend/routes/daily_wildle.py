from flask import Blueprint, request, jsonify
import csv
import os
import hmac
import hashlib
import pytz
import datetime as dt
from typing import Dict, List, Optional, Any

daily_wildle_bp = Blueprint('daily_wildle', __name__)

AUS_TZ = pytz.timezone("Australia/Melbourne")
SECRET = "change-me-please"

EPBC_ORDER = ["Present", "Vulnerable", "Endangered", "Critically Endangered"]
SIZE_ORDER = ["Very Large", "Large", "Medium", "Small"]
EPBC_RANK = {v: i for i, v in enumerate(EPBC_ORDER)}
SIZE_RANK = {v: i for i, v in enumerate(SIZE_ORDER)}

_SPECIES_ROWS: List[Dict[str, Any]] = []

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
    items = []
    for k, v in row.items():
        if k.startswith("habitat_"):
            s = str(v).strip().lower()
            if s in ("true", "1", "yes", "y"):
                items.append(k.replace("habitat_", ""))
    return sorted(items)

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
        raise ValueError("no species loaded")
    idx = _pick_daily_index(SECRET, _game_date_str(), len(_SPECIES_ROWS))
    return _SPECIES_ROWS[idx]

def _opaque_id(row: Dict[str, Any], date_str: str) -> str:
    key = f"{date_str}|{row.get('ScientificName','')}"
    return hmac.new(SECRET.encode(), key.encode(), hashlib.sha256).hexdigest()[:16]

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

def init_daily_wildle():
    global _SPECIES_ROWS

    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "australian wildle", "animal_details_top_animals_pruned.csv")

    _SPECIES_ROWS = _load_rows(csv_path)

    for r in _SPECIES_ROWS:
        r["CommonName"] = r.get("CommonName") or r.get("common_name") or ""
        r["ScientificName"] = r.get("ScientificName") or r.get("scientific_name") or ""

    _SPECIES_ROWS.sort(key=lambda r: (r.get("ScientificName",""), r.get("CommonName","")))

    for r in _SPECIES_ROWS:
        r["diet"] = _derive_diet(r)
        r["habitats"] = _derive_habitats(r)

@daily_wildle_bp.route('/today', methods=['GET'])
def game_today():
    try:
        date_str = _game_date_str()
        target = _daily_target()

        suggestions = []
        seen = set()

        today_name = (target.get("CommonName") or "").strip()
        if today_name:
            suggestions.append(today_name)
            seen.add(today_name)

        n = len(_SPECIES_ROWS)
        if n > 0:
            now = _today_au()
            days_checked = 1  # start from yesterday
            while len(suggestions) < 10 and days_checked < 365:  # safety cap
                date = now - dt.timedelta(days=days_checked)
                ds = date.strftime("%Y-%m-%d")
                idx = _pick_daily_index(SECRET, ds, n)
                row = _SPECIES_ROWS[idx]
                nm = (row.get("CommonName") or "").strip()
                if nm and nm not in seen:
                    suggestions.append(nm)
                    seen.add(nm)
                days_checked += 1
        
        suggestions = sorted(suggestions, key=lambda s: s.casefold())
        
        return jsonify({
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
                "animals": suggestions
            },
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daily_wildle_bp.route('/guess', methods=['POST'])
def game_guess():
    try:
        data = request.get_json()
        name = data.get('guess_name', '').strip().lower()
        guess_count = data.get('guess_count', 1)

        by_name = _by_common_name()
        guess_row = by_name.get(name)

        target = _daily_target()

        if not guess_row:
            if guess_count >= 10:
                target_snapshot = {
                    "CommonName": target.get("CommonName"),
                    "taxon_class_ET": target.get("taxon_class_ET"),
                    "EPBCThreatStatus": target.get("EPBCThreatStatus"),
                    "size_bucket": target.get("size_bucket"),
                    "activity_top": target.get("activity_top"),
                    "habitats": target.get("habitats"),
                    "diet": target.get("diet"),
                }
                feedback = _make_feedback(target, target, reveal=True)
                return jsonify({
                    "game_date": _game_date_str(),
                    "solved": False,
                    "game_over": True,
                    "guess": target_snapshot,
                    "feedback": feedback,
                    "correct_answer": target.get("CommonName"),
                    "message": f"Game over! The correct answer was: {target.get('CommonName')}"
                })
            return jsonify({"error": "unknown animal name"}), 404

        solved = (guess_row.get("CommonName") == target.get("CommonName"))

        guess_snapshot = {
            "CommonName": guess_row.get("CommonName"),
            "taxon_class_ET": guess_row.get("taxon_class_ET"),
            "EPBCThreatStatus": guess_row.get("EPBCThreatStatus"),
            "size_bucket": guess_row.get("size_bucket"),
            "activity_top": guess_row.get("activity_top"),
            "habitats": guess_row.get("habitats"),
            "diet": guess_row.get("diet"),
        }

        if solved or guess_count >= 10:
            feedback = _make_feedback(guess_row, target, reveal=True)
            if not solved and guess_count >= 10:
                return jsonify({
                    "game_date": _game_date_str(),
                    "solved": False,
                    "game_over": True,
                    "guess": guess_snapshot,
                    "feedback": feedback,
                    "correct_answer": target.get("CommonName"),
                    "message": f"Game over! The correct answer was: {target.get('CommonName')}"
                })
        else:
            feedback = _make_feedback(guess_row, target, reveal=False)

        return jsonify({
            "game_date": _game_date_str(),
            "solved": solved,
            "game_over": solved or guess_count >= 10,
            "guess": guess_snapshot,
            "feedback": feedback
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daily_wildle_bp.route('/history', methods=['GET'])
def game_history():
    try:
        limit = int(request.args.get('limit', 30))
        out = []
        n = len(_SPECIES_ROWS)
        if n == 0:
            return jsonify(out)

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
        return jsonify(out)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
