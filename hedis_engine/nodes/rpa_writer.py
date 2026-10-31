import json
from pathlib import Path

def generate_rpa_batch_node(state: dict) -> dict:
    if hasattr(state, "processed_gaps"):
        gaps = state.processed_gaps or []
    elif isinstance(state, dict):
        gaps = state.get("processed_gaps", [])
    else:
        gaps = getattr(state, "processed_gaps", [])
        
    if not gaps:
        print("Skipping RPA payload generation: No processed gaps found.")
        return {"rpa_payload_path": None}
        
    outbox_dir = Path("data/shared_rpa_outbox")
    outbox_dir.mkdir(parents=True, exist_ok=True)
    
    gap = gaps[0]
    if hasattr(gap, "model_dump"):
        gap_dict = gap.model_dump()
    elif hasattr(gap, "dict"):
        gap_dict = gap.dict()
    elif isinstance(gap, dict):
        gap_dict = gap
    else:
        gap_dict = {
            "member_id": getattr(gap, "member_id", "UNKNOWN"),
            "measure": getattr(gap, "measure", "UNKNOWN"),
            "evidence_value": getattr(gap, "evidence_value", "UNKNOWN"),
            "gap_status": getattr(gap, "gap_status", "UNKNOWN")
        }
        
    payload = {
        "target_system": "EZCAP_CLAIMS_UI",
        "action": "CLOSE_CARE_GAP",
        "member_id": gap_dict.get("member_id"),
        "measure": gap_dict.get("measure"),
        "evidence_value": gap_dict.get("evidence_value"),
        "status": "READY_FOR_RPA_BOT"
    }
    
    member_id = gap_dict.get("member_id", "BATCH")
    measure = gap_dict.get("measure", "GENERAL")
    file_path = outbox_dir / f"RPA_BATCH_{member_id}_{measure}.json"
    
    with open(file_path, "w") as f:
        json.dump(payload, f, indent=2)
        
    print(f"Generated RPA Batch Payload: {file_path}")
    return {"rpa_payload_path": str(file_path)}