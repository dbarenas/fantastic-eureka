import os
from neo4j import GraphDatabase

# Database connection details from environment variables
uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
user = os.environ.get("NEO4J_USER", "neo4j")
password = os.environ.get("NEO4J_PASSWORD", "neo4j_pass")
driver = GraphDatabase.driver(uri, auth=(user, password))

CLASSIFY_REL = """
MERGE (f:Fact {id:$id})
SET f.text=$text, f.source=$source
WITH f
MERGE (fac:Factor {id:$factor})
MERGE (fac)-[:HAS_FACT]->(f)
MERGE (a:Agent {id:$agent_id})-[:OWNS]->(f)
RETURN f.id AS id
"""

GET_AGENT_CONTEXT_QUERY = """
MATCH (a:Agent {id: $agent_id})-[:OWNS]->(f:Fact)
RETURN f.text AS text, f.source AS source
"""

def get_agent_context(agent_id: str):
    """Retrieves all facts owned by a specific agent."""
    with driver.session() as s:
        records = s.run(GET_AGENT_CONTEXT_QUERY, agent_id=agent_id).data()
        return records

def write_fact_with_factor(agent_id: str, fact_id: str, text: str, factor: str, source: str):
    """Writes a new fact to the database, linking it to a factor and an agent."""
    with driver.session() as s:
        rec = s.run(CLASSIFY_REL, id=fact_id, text=text, factor=factor, source=source, agent_id=agent_id).single()
        return rec["id"]
