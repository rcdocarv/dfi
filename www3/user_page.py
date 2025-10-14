import panel as pn
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import json

pn.extension()

# ---------------------------
# Conexão MongoDB
# ---------------------------
client = AsyncIOMotorClient('mongodb://localhost:27017/')
db = client.daphi_stakeholders
users_collection = db.users

# ---------------------------
# Busca documento async
# ---------------------------
async def fetch_user_document(username):
    return await users_collection.find_one({"username": username})

# ---------------------------
# Accordion com JSON puro
# ---------------------------
def create_user_json_accordion(user_doc):
    if not user_doc:
        return pn.pane.Markdown("**Nenhum dado encontrado para este utilizador**")
    
    doc_copy = dict(user_doc)
    doc_copy['_id'] = str(doc_copy.get('_id'))
    for k, v in doc_copy.items():
        if hasattr(v, "isoformat"):  # datetime -> string
            doc_copy[k] = v.isoformat()
        elif isinstance(v, (bytes, bytearray)):  # BinData -> hex string
            doc_copy[k] = v.hex()
    
    json_str = json.dumps(doc_copy, indent=4, ensure_ascii=False)
    
    return pn.Accordion(
        ("Documento Completo", pn.pane.Markdown(f"```json\n{json_str}\n```", width=800, sizing_mode="stretch_width")),
        active=[0],
        width=820
    )

# ---------------------------
# Layout principal do utilizador
# ---------------------------
def get_user_content(username):
    async def async_layout():
        user_doc = await fetch_user_document(username)
        accordion = create_user_json_accordion(user_doc)
        return pn.Column(
            pn.pane.Markdown(f"## Dados do Utilizador: **{username}**"),
            accordion,
            sizing_mode="stretch_width"
        )
    
    return pn.bind(async_layout)
