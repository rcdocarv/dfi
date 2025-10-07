import panel as pn
from panel.io import state
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
pn.extension(sizing_mode="stretch_width")

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

# Classe pro estado do menu (simples e funcional)
class MenuState(param.Parameterized):
    selected = param.ObjectSelector(default='user', objects=['user', 'systems', 'help'])

menu_state = MenuState()  # Instância

# Importar os módulos das páginas (aqui é a única mudança!)
from user_page import get_user_content
from systems_page import get_systems_content
from help_page import get_help_content

# Função pro conteúdo dinâmico (agora chama os módulos separados)
def get_content(selected):
    if selected == 'user':
        return get_user_content(auth.current_user)  # Passa o usuário pro módulo
    elif selected == 'systems':
        return get_systems_content()
    elif selected == 'help':
        return get_help_content()
    else:
        return pn.pane.Markdown("# Dashboard Inicial\nSelecione um menu na sidebar.")

# Conteúdo bound (aqui o fix: pn.bind faz o reativo automático)
main_content = pn.bind(get_content, menu_state.param.selected)

# Botões do menu (ícones, light pra moderno)
user_btn = pn.widgets.Button(name='👤 Usuário', button_type='light', width=200, height=40)
systems_btn = pn.widgets.Button(name='⚙️ Sistemas', button_type='light', width=200, height=40)
help_btn = pn.widgets.Button(name='❓ Ajuda', button_type='light', width=200, height=40)

# Callbacks simples (só setam o estado — bind cuida do resto)
def on_user_click(event): menu_state.selected = 'user'
def on_systems_click(event): menu_state.selected = 'systems'
def on_help_click(event): menu_state.selected = 'help'

user_btn.on_click(on_user_click)
systems_btn.on_click(on_systems_click)
help_btn.on_click(on_help_click)

# Sidebar: Header + botões com ar + logout (visible=False inicial)
sidebar_menu = pn.Column(
    pn.pane.HTML('<h3 style="color: #1976d2; text-align: center; margin: 20px 0;">Meu App</h3>'),
    pn.layout.Divider(),
    user_btn,
    pn.layout.Spacer(height=10),
    systems_btn,
    pn.layout.Spacer(height=10),
    help_btn,
    pn.layout.Spacer(height=20),
    logout_btn,  # Adicionado logout no final
    sizing_mode='stretch_height',
    visible=False  # Inicialmente invisível pra evitar erro
)

# Dashboard principal (agora usa o main_content)
def dashboard_view():
    return pn.Column(
        main_content,
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
        # Atualiza o layout principal
        def update_layout():
            template.main[:] = [dynamic_layout(auth.is_logged_in)]
            sidebar_menu.visible = True  # Mostra sidebar
        state.curdoc.add_next_tick_callback(update_layout)
        password_input.value = ""

async def logout_callback(event):
    success, msg = await auth.logout_user()
    message.object = f"**{msg}**"
    def update_layout():
        template.main[:] = [dynamic_layout(auth.is_logged_in)]
        sidebar_menu.visible = False  # Esconde sidebar
    state.curdoc.add_next_tick_callback(update_layout)

# Configurar callbacks com execução assíncrona
def setup_callbacks():
    register_btn.on_click(lambda event: asyncio.create_task(register_callback(event)))
    login_btn.on_click(lambda event: asyncio.create_task(login_callback(event)))
    logout_btn.on_click(lambda event: asyncio.create_task(logout_callback(event)))

def dynamic_layout(is_logged_in):
    if is_logged_in:
        return dashboard_view()
    else:
        return login_view()

# Template principal (mudado pra MaterialTemplate pra combinar com sidebar)
template = pn.template.MaterialTemplate(
    title="Sistema daphi_Stakeholders",
    header_background="#2E86AB",
    sidebar=[sidebar_menu],  # Adiciona sidebar com visible=False inicial
)

# Inicializar a aplicação
def init_app():
    setup_callbacks()
    template.main[:] = [pn.bind(dynamic_layout, auth.param.is_logged_in)]
    # Não seta sidebar = [] aqui — já tá no constructor
    return template

# Servir a aplicação
app = init_app()
app.servable()