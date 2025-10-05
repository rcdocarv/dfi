import panel as pn
import param
import bcrypt
import secrets
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from bson import ObjectId

# Configurações para HTTPS
#pn.config.ssl_verify = True
#pn.config.require_https = True

# Configuração do Panel
pn.extension()

# Conexão com MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017/')
db = client.daphi_stakeholders
users_collection = db.users
sessions_collection = db.sessions

# Gerenciador de Estado e Autenticação
class AuthManager(param.Parameterized):
    current_user = param.String(default="")
    is_logged_in = param.Boolean(default=False)
    session_token = param.String(default="")
    
    async def register_user(self, username, password):
        # Verificar se usuário já existe
        existing_user = await users_collection.find_one({"username": username})
        if existing_user:
            return False, "Usuário já existe"
        
        # Hash da senha com bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Criar usuário no MongoDB
        user_data = {
            "username": username,
            "password_hash": hashed_password,
            "created_at": datetime.utcnow(),
            "last_login": None
        }
        
        result = await users_collection.insert_one(user_data)
        return True, f"Usuário {username} criado com sucesso"
    
    async def login_user(self, username, password):
        # Buscar usuário no MongoDB
        user = await users_collection.find_one({"username": username})
        if not user:
            return False, "Usuário não encontrado"
        
        # Verificar senha
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            # Criar sessão
            session_token = secrets.token_urlsafe(32)
            session_data = {
                "user_id": user['_id'],
                "username": username,
                "token": session_token,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=24)
            }
            
            await sessions_collection.insert_one(session_data)
            
            # Atualizar último login
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
            # Remover sessão do MongoDB
            await sessions_collection.delete_one({"token": self.session_token})
        
        self.current_user = ""
        self.is_logged_in = False
        self.session_token = ""
        return True, "Logout bem-sucedido"
    
    async def validate_session(self, token):
        if not token:
            return False
        
        session = await sessions_collection.find_one({"token": token})
        if session and session['expires_at'] > datetime.utcnow():
            self.current_user = session['username']
            self.is_logged_in = True
            self.session_token = token
            return True
        return False

# Instância do gerenciador de auth
auth = AuthManager()

# Componentes da UI
username_input = pn.widgets.TextInput(placeholder="Usuário", width=200)
password_input = pn.widgets.PasswordInput(placeholder="Senha", width=200)
register_btn = pn.widgets.Button(name="Registrar", button_type="primary")
login_btn = pn.widgets.Button(name="Login", button_type="success")
logout_btn = pn.widgets.Button(name="Logout", button_type="warning")
message = pn.pane.Markdown("")

# Dashboard principal
def dashboard_view():
    return pn.Column(
        pn.pane.Markdown(f"# 🎉 Bem-vindo, {auth.current_user}!"),
        pn.pane.Markdown("### Você está logado no sistema"),
        pn.layout.Divider(),
        pn.widgets.Button(name="Meu Perfil", button_type="primary"),
        pn.widgets.Button(name="Configurações", button_type="primary"),
        logout_btn,
        sizing_mode="stretch_width"
    )

# Página de login/registro
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

# Callbacks assíncronos
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

async def logout_callback(event):
    success, msg = await auth.logout_user()
    message.object = f"**{msg}**"

# Configurar callbacks com execução assíncrona
def setup_callbacks():
    register_btn.on_click(lambda event: asyncio.create_task(register_callback(event)))
    login_btn.on_click(lambda event: asyncio.create_task(login_callback(event)))
    logout_btn.on_click(lambda event: asyncio.create_task(logout_callback(event)))

# Layout dinâmico
@pn.depends(auth.param.is_logged_in, watch=True)
def dynamic_layout(is_logged_in):
    if is_logged_in:
        return dashboard_view()
    else:
        return login_view()

# Template principal
template = pn.template.BootstrapTemplate(
    title="Sistema daphi_Stakeholders",
    header_background="#2E86AB",
)

# Inicializar a aplicação
def init_app():
    setup_callbacks()
    template.main.append(dynamic_layout)
    return template

# Servir a aplicação
app = init_app()
app.servable()