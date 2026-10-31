from typing import List, Optional
from pydantic import BaseModel

class CareGap(BaseModel):
    member_id: str
    name: str
    measure: str
    gap_status: str
    evidence_value: Optional[str] = None

class HedisState(BaseModel):
    unprocessed_gaps: List[CareGap] = []
    processed_gaps: List[CareGap] = []
    rpa_payload_path: Optional[str] = None