import panel as pn
from panel.io import state
import param
import bcrypt
import secrets
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from bson import ObjectId

# Configuração do Panel
pn.extension(sizing_mode="stretch_width")

# Conexão com MongoDB
# ATENÇÃO: Verifique a conexão. Se for um ambiente de produção, use variáveis de ambiente.
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
    
    # ... (validate_session omitido para brevidade, mas está ok)

# Instância do gerenciador de auth
auth = AuthManager()

# Componentes da UI
username_input = pn.widgets.TextInput(placeholder="Usuário", width=200)
password_input = pn.widgets.PasswordInput(placeholder="Senha", width=200)
register_btn = pn.widgets.Button(name="Registrar", button_type="primary")
login_btn = pn.widgets.Button(name="Login", button_type="success")
logout_btn = pn.widgets.Button(name="Logout", button_type="warning")
message = pn.pane.Markdown("")

# Classe pro estado do menu
class MenuState(param.Parameterized):
    selected = param.ObjectSelector(default='user', objects=['user', 'systems', 'help'])

menu_state = MenuState()

# Função pro conteúdo dinâmico do MAIN
def get_content(selected):
    if selected == 'user':
        return pn.pane.Markdown(f"""# Perfil do Usuário
        Bem-vindo ao seu perfil, **{auth.current_user}**!
        ...""")
    elif selected == 'systems':
        return pn.pane.Markdown("# Sistemas\nGerencie os sistemas disponíveis.\n...")
    elif selected == 'help':
        return pn.pane.Markdown("# Ajuda\nPrecisa de suporte? Consulte nossa documentação.\n...")
    else:
        return pn.pane.Markdown("# Dashboard Inicial\nSelecione um menu na sidebar.")

# Conteúdo bound
main_content = pn.bind(get_content, menu_state.param.selected)

# Botões do menu
user_btn = pn.widgets.Button(name='👤 Usuário', button_type='light', width=200, height=40)
systems_btn = pn.widgets.Button(name='⚙️ Sistemas', button_type='light', width=200, height=40)
help_btn = pn.widgets.Button(name='❓ Ajuda', button_type='light', width=200, height=40)

# Callbacks simples
user_btn.on_click(lambda event: setattr(menu_state, 'selected', 'user'))
systems_btn.on_click(lambda event: setattr(menu_state, 'selected', 'systems'))
help_btn.on_click(lambda event: setattr(menu_state, 'selected', 'help'))

# --- REORGANIZAÇÃO DA SIDEBAR PARA VISIBILIDADE DINÂMICA ---

# Agrupa os botões de navegação
menu_buttons = pn.Column(
    user_btn,
    pn.layout.Spacer(height=10),
    systems_btn,
    pn.layout.Spacer(height=10),
    help_btn,
    pn.layout.Spacer(height=20),
    logout_btn,
)

# Conteúdo dinâmico da Sidebar, dependente do estado de login
@pn.depends(auth.param.is_logged_in)
def get_sidebar_content(is_logged_in):
    # O título e o separador (divider) sempre são mostrados
    header = pn.Column(
        pn.pane.HTML('<h3 style="color: #1976d2; text-align: center; margin: 20px 0;">Meu App</h3>'),
        pn.layout.Divider()
    )
    
    if is_logged_in:
        # Se logado, retorna o header e os botões
        return pn.Column(header, menu_buttons, sizing_mode='stretch_height')
    else:
        # Se deslogado, retorna o header e uma mensagem
        return pn.Column(header, pn.pane.Markdown("Faça login para acessar o menu."), sizing_mode='stretch_height')

# --- REORGANIZAÇÃO DA SIDEBAR (FIM) ---

# Dashboard principal
def dashboard_view():
    return pn.Column(main_content, sizing_mode="stretch_width")

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
        # Apenas atualiza o layout principal. A sidebar se atualiza automaticamente.
        def update_layout():
            template.main[:] = [dynamic_layout(auth.is_logged_in)]
            # REMOVIDA: sidebar_menu.visible = True
        state.curdoc.add_next_tick_callback(update_layout)
        password_input.value = ""
        username_input.value = ""

async def logout_callback(event):
    success, msg = await auth.logout_user()
    message.object = f"**{msg}**"
    # Apenas atualiza o layout principal. A sidebar se atualiza automaticamente.
    def update_layout():
        template.main[:] = [dynamic_layout(auth.is_logged_in)]
        # REMOVIDA: sidebar_menu.visible = False
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

# Template principal (MaterialTemplate)
template = pn.template.MaterialTemplate(
    title="Sistema daphi_Stakeholders",
    header_background="#2E86AB",
    # Adicionamos a função bound (get_sidebar_content) como conteúdo da sidebar
    sidebar=[get_sidebar_content],
)

# Inicializar a aplicação
def init_app():
    setup_callbacks()
    # Vincula o layout principal ao estado de login (is_logged_in)
    template.main[:] = [pn.bind(dynamic_layout, auth.param.is_logged_in)]
    return template

# Servir a aplicação
app = init_app()
app.servable()