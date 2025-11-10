import uuid
import json
import re
from .neo import get_agent_context, write_fact_with_factor
from .llm import call_llm
from .state import GraphState, Turn

def researcher(state: GraphState) -> GraphState:
    # 1️⃣ Obtener contexto desde Neo4j
    ctx = get_agent_context(state.agent_id)

    # 2️⃣ Si no hay suficiente contexto, buscar en ChatGPT
    if not ctx or len(ctx) < 2:
        search_prompt = f"""
Eres un analista financiero.
Investiga sobre los factores para elegir inversiones en ETFs.
Clasifica la información en tres categorías:
1. Perfil de Inversión
2. Producto (ETF)
3. Operativa y Mercado

Responde en formato JSON con tres claves: perfil, producto, operativa.
"""
        response = call_llm(search_prompt)
        # Extraer el JSON

        match = re.search(r"\{.*\}", response, re.S)
        if match:
            data = json.loads(match.group(0))
            # 3️⃣ Escribir en la knowledge base
            for factor, facts in data.items():
                if isinstance(facts, list):
                    for f in facts:
                        write_fact_with_factor(
                            agent_id=state.agent_id,
                            fact_id=str(uuid.uuid4()),
                            text=f.strip(),
                            factor=factor,
                            source="chatgpt-auto"
                        )
            # Recargar contexto
            ctx = get_agent_context(state.agent_id)

    # 4️⃣ Llamada LLM con contexto actualizado
    bullets = "\n".join(f"- {c['text']}" for c in ctx)
    prompt = f"""
Usa la siguiente información clasificada en Neo4j.
Genera un análisis estructurado sobre cómo seleccionar ETFs según los tres factores.

[Contexto]
{bullets}

[Pregunta]
{state.question}
"""
    answer = call_llm(prompt)

    state.messages.append(Turn(role="agent", agent_id=state.agent_id, content=answer))
    state.context = ctx
    return state
