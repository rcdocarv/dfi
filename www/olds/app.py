import panel as pn
import asyncio
import os
from auth import auth
from dashboard import dashboard_view, logout_btn

# Configuração do Panel
pn.config.ssl_certfile = os.getenv('SSL_CERTFILE', '')
pn.config.ssl_keyfile = os.getenv('SSL_KEYFILE', '')
pn.config.session_key = os.getenv('SESSION_KEY', 'secret-key-change-in-production')
pn.config.proxy_enabled = True
pn.config.cookie_secret = os.getenv('COOKIE_SECRET', 'another-secret-change-in-production')
pn.extension()

# Componentes de login
username_input = pn.widgets.TextInput(placeholder="Usuário", width=200)
password_input = pn.widgets.PasswordInput(placeholder="Senha", width=200)
register_btn = pn.widgets.Button(name="Registrar", button_type="primary")
login_btn = pn.widgets.Button(name="Login", button_type="success")
message = pn.pane.Markdown("")

# Página de login
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

# Callbacks
async def register_callback(event):
    if not username_input.value or not password_input.value:
        message.object = "**Erro**: Preencha todos os campos"
        return
    success, msg = await auth.register_user(username_input.value, password_input.value)
    message.object = f"**{msg}**"
    if success:
        username_input.value, password_input.value = "", ""

async def login_callback(event):
    if not username_input.value or not password_input.value:
        message.object = "**Erro**: Preencha todos os campos"
        return
    success, msg = await auth.login_user(username_input.value, password_input.value)
    message.object = f"**{msg}**"
    if success:
        username_input.value, password_input.value = "", ""

async def logout_callback(event):
    success, msg = await auth.logout_user()
    message.object = f"**{msg}**"

def setup_callbacks():
    register_btn.on_click(lambda event: asyncio.create_task(register_callback(event)))
    login_btn.on_click(lambda event: asyncio.create_task(login_callback(event)))
    logout_btn.on_click(lambda event: asyncio.create_task(logout_callback(event)))

# Layout dinâmico
@pn.depends(auth.param.is_logged_in, watch=True)
def dynamic_layout(is_logged_in):
    return dashboard_view() if is_logged_in else login_view()

# Template principal
template = pn.template.BootstrapTemplate(
    title="Daphi",
    header_background="#2E86AB",
)

def init_app():
    setup_callbacks()
    template.main.append(dynamic_layout)
    return template

app = init_app()
app.servable()
