# app.py
import panel as pn
import param
import asyncio
from auth_manager import AuthManager

# Configuração do Panel
pn.extension()

# Instância do gerenciador de auth
auth = AuthManager()

# Componentes da UI para login
username_input = pn.widgets.TextInput(placeholder="Usuário", width=200)
password_input = pn.widgets.PasswordInput(placeholder="Senha", width=200)
register_btn = pn.widgets.Button(name="Registrar", button_type="primary")
login_btn = pn.widgets.Button(name="Login", button_type="success")
message = pn.pane.Markdown("")

# Importar módulos
from modules.dashboard import DashboardModule
from modules.perfil import PerfilModule
from modules.relatorios import RelatoriosModule
from modules.configuracao import ConfiguracaoModule

# Instanciar módulos
dashboard_module = DashboardModule(auth)
perfil_module = PerfilModule(auth)
relatorios_module = RelatoriosModule(auth)
configuracao_module = ConfiguracaoModule(auth)

# Template principal - SEM SIDEBAR INICIALMENTE
template = pn.template.BootstrapTemplate(
    title="Sistema daphi_Stakeholders",
    header_background="#2E86AB",
)

# Página de login/registro (SEM SIDEBAR)
def login_view():
    return pn.Column(
        pn.pane.Markdown("# 🔐 Sistema de Autenticação"),
        pn.pane.Markdown("### Registre-se ou faça login"),
        username_input,
        password_input,
        pn.Row(register_btn, login_btn),
        message,
        sizing_mode="stretch_width",
        styles={'padding': '50px', 'max-width': '400px', 'margin': '0 auto'}
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

# Configurar callbacks
def setup_callbacks():
    register_btn.on_click(lambda event: asyncio.create_task(register_callback(event)))
    login_btn.on_click(lambda event: asyncio.create_task(login_callback(event)))

# Layout dinâmico
@pn.depends(auth.param.is_logged_in, watch=True)
def dynamic_layout(is_logged_in):
    if is_logged_in:
        # Configurar template para dashboard COM SIDEBAR
        template.sidebar_width = 280
        template.collapsed_sidebar = False
        
        # Limpar e adicionar sidebar apenas quando logado
        template.sidebar.clear()
        template.sidebar.append(dashboard_module.create_sidebar())
        
        return dashboard_module.view()
    else:
        # Remover sidebar quando no login
        template.sidebar.clear()
        template.sidebar_width = 0
        
        return login_view()

# Inicializar a aplicação
def init_app():
    setup_callbacks()
    template.main.append(dynamic_layout)
    return template

# Servir a aplicação
app = init_app()
app.servable()