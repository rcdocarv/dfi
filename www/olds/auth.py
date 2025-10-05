import panel as pn
import param
import bcrypt
import secrets
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Conexão com MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017/')
db = client.daphi_stakeholders
users_collection = db.users
sessions_collection = db.sessions

# ----------------------------
# Gerenciador de autenticação
# ----------------------------
class AuthManager(param.Parameterized):
    current_user = param.String(default="")
    is_logged_in = param.Boolean(default=False)
    session_token = param.String(default="")

    async def register_user(self, username, password):
        existing_user = await users_collection.find_one({"username": username})
        if existing_user:
            return False, "Usuário já existe"

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "username": username,
            "password_hash": hashed_password,
            "created_at": datetime.utcnow(),
            "last_login": None,
        }
        await users_collection.insert_one(user_data)
        return True, f"Usuário {username} criado com sucesso"

    async def login_user(self, username, password):
        user = await users_collection.find_one({"username": username})
        if not user:
            return False, "Usuário não encontrado"

        if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
            session_token = secrets.token_urlsafe(32)
            session_data = {
                "user_id": user["_id"],
                "username": username,
                "token": session_token,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=24),
            }
            await sessions_collection.insert_one(session_data)

            await users_collection.update_one(
                {"_id": user["_id"]}, {"$set": {"last_login": datetime.utcnow()}}
            )

            self.current_user = username
            self.is_logged_in = True
            self.session_token = session_token
            return True, "Login bem-sucedido"
        return False, "Senha incorreta"

    async def logout_user(self):
        if self.session_token:
            await sessions_collection.delete_one({"token": self.session_token})
        self.current_user, self.is_logged_in, self.session_token = "", False, ""
        return True, "Logout bem-sucedido"

# ----------------------------
# UI de Login
# ----------------------------
auth = AuthManager()

username_input = pn.widgets.TextInput(placeholder="Usuário", width=200)
password_input = pn.widgets.PasswordInput(placeholder="Senha", width=200)
register_btn = pn.widgets.Button(name="Registrar", button_type="primary")
login_btn = pn.widgets.Button(name="Login", button_type="success")
message = pn.pane.Markdown("")

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

def setup_callbacks():
    register_btn.on_click(lambda e: asyncio.create_task(register_callback(e)))
    login_btn.on_click(lambda e: asyncio.create_task(login_callback(e)))

def login_view():
    setup_callbacks()
    return pn.Column(
        pn.pane.Markdown("# 🔐 Sistema de Autenticação", align="center"),
        pn.pane.Markdown("### Registre-se ou faça login", align="center"),
        pn.Row(username_input, align="center"),
        pn.Row(password_input, align="center"),
        pn.Row(register_btn, login_btn, align="center"),
        message,
        sizing_mode="stretch_width",
    )
