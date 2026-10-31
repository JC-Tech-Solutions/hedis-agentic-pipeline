import duckdb
from hedis_engine.schemas.hedis_types import CareGap

def fetch_gaps_node(state: dict) -> dict:
    conn = duckdb.connect("data/hedis.duckdb")
    results = conn.execute(
        "SELECT member_id, member_name, measure_code, gap_status FROM fct_hedis_bpd"
    ).fetchall()
    conn.close()
    
    gaps = [
        CareGap(
            member_id=r[0],
            name=r[1],
            measure=r[2],
            gap_status=r[3]
        ) 
        for r in results
    ]
    
    return {"unprocessed_gaps": gaps}