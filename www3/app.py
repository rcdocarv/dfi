# app.py
import panel as pn
from panel.io import state
import param
import bcrypt
import secrets
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from bson import ObjectId

# Panel
pn.extension(sizing_mode="stretch_width")

# MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017/')
db = client.daphi_stakeholders
users_collection = db.users
sessions_collection = db.sessions

# ---------------------------
# AuthManager original
# ---------------------------
class AuthManager(param.Parameterized):
    current_user = param.String(default="")
    is_logged_in = param.Boolean(default=False)
    session_token = param.String(default="")
    
    async def register_user(self, username, password):
        existing_user = await users_collection.find_one({"username": username})
        if existing_user:
            return False, "Usuário já existe"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            "username": username,
            "password_hash": hashed_password,
            "created_at": datetime.utcnow(),
            "last_login": None
        }
        await users_collection.insert_one(user_data)
        return True, f"Usuário {username} criado com sucesso"

    async def login_user(self, username, password):
        user = await users_collection.find_one({"username": username})
        if not user:
            return False, "Usuário não encontrado"
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            session_token = secrets.token_urlsafe(32)
            session_data = {
                "user_id": user['_id'],
                "username": username,
                "token": session_token,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=24)
            }
            await sessions_collection.insert_one(session_data)
            await users_collection.update_one(
                {"_id": user['_id']},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            self.current_user = username
            self.is_logged_in = True
            self.session_token = session_token
            return True, "Login bem-sucedido"
        else:
            return False, "Senha incorreta"

    async def logout_user(self):
        if self.session_token:
            await sessions_collection.delete_one({"token": self.session_token})
        self.current_user = ""
        self.is_logged_in = False
        self.session_token = ""
        return True, "Logout bem-sucedido"

auth = AuthManager()

# ---------------------------
# Widgets de login
# ---------------------------
username_input = pn.widgets.TextInput(placeholder="Usuário", width=200)
password_input = pn.widgets.PasswordInput(placeholder="Senha", width=200)
register_btn = pn.widgets.Button(name="Registrar", button_type="primary")
login_btn = pn.widgets.Button(name="Login", button_type="success")
logout_btn = pn.widgets.Button(name="Logout", button_type="warning")
message = pn.pane.Markdown("")

# ---------------------------
# Import dashboard
# ---------------------------
from dash import dashboard_template

# ---------------------------
# Layouts
# ---------------------------
def login_view():
    return pn.Column(
        pn.pane.Markdown("# 🔐 Sistema de Autenticação"),
        pn.pane.Markdown("### Registre-se ou faça login"),
        username_input,
        password_input,
        pn.Row(register_btn, login_btn),
        message,
        sizing_mode="stretch_width"
    )

def dynamic_layout(is_logged_in):
    if is_logged_in:
        return dashboard_template(auth.current_user, logout_btn)
    else:
        return login_view()

# ---------------------------
# Callbacks assíncronos
# ---------------------------
async def register_callback(event):
    if not username_input.value or not password_input.value:
        message.object = "**Erro**: Preencha todos os campos"
        return
    success, msg = await auth.register_user(username_input.value, password_input.value)
    message.object = f"**{msg}**"
    if success:
        username_input.value = ""
        password_input.value = ""

async def login_callback(event):
    if not username_input.value or not password_input.value:
        message.object = "**Erro**: Preencha todos os campos"
        return
    success, msg = await auth.login_user(username_input.value, password_input.value)
    message.object = f"**{msg}**"
    if success:
        username_input.value = ""
        password_input.value = ""
        def update_layout():
            template.main[:] = [dynamic_layout(auth.is_logged_in)]
        state.curdoc.add_next_tick_callback(update_layout)

async def logout_callback(event):
    await auth.logout_user()
    message.object = "**Logout realizado**"
    def update_layout():
        template.main[:] = [dynamic_layout(auth.is_logged_in)]
    state.curdoc.add_next_tick_callback(update_layout)

# ---------------------------
# Setup callbacks
# ---------------------------
def setup_callbacks():
    register_btn.on_click(lambda event: asyncio.create_task(register_callback(event)))
    login_btn.on_click(lambda event: asyncio.create_task(login_callback(event)))
    logout_btn.on_click(lambda event: asyncio.create_task(logout_callback(event)))

setup_callbacks()

# ---------------------------
# Template principal
# ---------------------------
template = pn.template.MaterialTemplate(
    title="Sistema daphi_Stakeholders",
    header_background="#2E86AB",
)
template.main[:] = [pn.bind(dynamic_layout, auth.param.is_logged_in)]

# Servir aplicação
template.servable()
