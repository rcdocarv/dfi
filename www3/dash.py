import panel as pn
import param

# Import do user_page async
from user_page import get_user_content
from systems_page import get_systems_content
from help_page import get_help_content

pn.extension(sizing_mode="stretch_width")

# ---------------------------
# Estado do menu
# ---------------------------
class MenuState(param.Parameterized):
    selected = param.ObjectSelector(default='user', objects=['user', 'systems', 'help'])

menu_state = MenuState()

# ---------------------------
# Função que retorna conteúdo dinâmico
# ---------------------------
def get_content(selected, current_user):
    if selected == 'user':
        return get_user_content(current_user)  # retorna pn.bind(async)
    elif selected == 'systems':
        return systems_page_layout()  # função que retorna Viewable
    elif selected == 'help':
        return help_page_layout()  # função que retorna Viewable
    else:
        return pn.pane.Markdown("# Dashboard Inicial\nSelecione um menu na sidebar.")

# ---------------------------
# Bind reativo
# ---------------------------
def bind_content(current_user):
    return pn.bind(get_content, menu_state.param.selected, current_user)

# ---------------------------
# Botões do menu
# ---------------------------
user_btn = pn.widgets.Button(name='👤 Usuário', button_type='light', width=200, height=40)
systems_btn = pn.widgets.Button(name='⚙️ Sistemas', button_type='light', width=200, height=40)
help_btn = pn.widgets.Button(name='❓ Ajuda', button_type='light', width=200, height=40)

user_btn.on_click(lambda event: setattr(menu_state, "selected", "user"))
systems_btn.on_click(lambda event: setattr(menu_state, "selected", "systems"))
help_btn.on_click(lambda event: setattr(menu_state, "selected", "help"))

# ---------------------------
# Sidebar com logout
# ---------------------------
def sidebar_menu(logout_btn):
    return pn.Column(
        pn.pane.HTML('<h3 style="color: #1976d2; text-align: center; margin: 20px 0;">Meu App</h3>'),
        pn.layout.Divider(),
        user_btn,
        pn.layout.Spacer(height=10),
        systems_btn,
        pn.layout.Spacer(height=10),
        help_btn,
        pn.layout.Spacer(height=20),
        logout_btn,
        sizing_mode='stretch_height'
    )

# ---------------------------
# Função principal do dashboard
# ---------------------------
def dashboard_template(current_user, logout_btn):
    sidebar = sidebar_menu(logout_btn)
    main_content = bind_content(current_user)  # retorna pn.bind(async)

    layout = pn.Row(
        sidebar,
        pn.layout.Spacer(width=10),
        main_content,
        sizing_mode="stretch_both"
    )
    return layout

# ---------------------------
# Placeholder para páginas de sistemas e ajuda
# ---------------------------
def systems_page_layout():
    return pn.Column(
        pn.pane.Markdown("## Página de Sistemas"),
        pn.pane.Markdown("Conteúdo dos sistemas aqui..."),
        sizing_mode="stretch_width"
    )

def help_page_layout():
    return pn.Column(
        pn.pane.Markdown("## Página de Ajuda"),
        pn.pane.Markdown("Conteúdo de ajuda aqui..."),
        sizing_mode="stretch_width"
    )
