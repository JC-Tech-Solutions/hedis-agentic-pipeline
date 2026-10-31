from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from hedis_engine.schemas.hedis_types import HedisState
from hedis_engine.nodes.gap_fetcher import fetch_gaps_node
from hedis_engine.nodes.extractor import extract_vitals_node
from hedis_engine.nodes.rpa_writer import generate_rpa_batch_node

def run_pipeline():
    memory = MemorySaver()

    workflow = StateGraph(HedisState)

    # Add nodes
    workflow.add_node("fetch_gaps", fetch_gaps_node)
    workflow.add_node("extract_vitals", extract_vitals_node)
    workflow.add_node("rpa_writer", generate_rpa_batch_node)

    # Define edges
    workflow.set_entry_point("fetch_gaps")
    workflow.add_edge("fetch_gaps", "extract_vitals")
    workflow.add_edge("extract_vitals", "rpa_writer")
    workflow.add_edge("rpa_writer", END)

    app = workflow.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": "hedis_batch_run_01"}}
    
    # Initialize with default keys so Pydantic validation is happy from the start
    initial_state = {
        "unprocessed_gaps": [],
        "processed_gaps": [],
        "rpa_payload_path": None
    }
    
    final_state = app.invoke(initial_state, config=config)
    print("✅ Execution complete.")
    
    # Handle output whether dict or pydantic model
    payload_path = final_state.get("rpa_payload_path") if isinstance(final_state, dict) else getattr(final_state, "rpa_payload_path", None)
    print(f"Generated RPA Batch Payload: {payload_path}")

if __name__ == "__main__":
    run_pipeline()