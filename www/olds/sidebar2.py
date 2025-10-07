import panel as pn
import param  # Pra estado reativo (vem com Panel)

pn.extension(sizing_mode="stretch_width")  # Layout responsivo

# Classe pro estado do menu (simples e funcional)
class MenuState(param.Parameterized):
    selected = param.ObjectSelector(default='user', objects=['user', 'systems', 'help'])

menu_state = MenuState()  # Instância

# Função pro conteúdo dinâmico (só texto, como querias)
def get_content(selected):
    if selected == 'user':
        return pn.pane.Markdown("""
        # Perfil do Usuário
        
        Bem-vindo ao seu perfil! Aqui você pode gerenciar suas configurações pessoais.
        
        - Nome: João Silva
        - Email: joao@email.com
        - Último login: 05/10/2025
        """)
    elif selected == 'systems':
        return pn.pane.Markdown("""
        # Sistemas
        
        Gerencie os sistemas disponíveis.
        
        - Sistema A: Status online
        - Sistema B: Manutenção em andamento
        - Sistema C: Offline
        """)
    elif selected == 'help':
        return pn.pane.Markdown("""
        # Ajuda
        
        Precisa de suporte? Consulte nossa documentação.
        
        - FAQ: Perguntas frequentes
        - Contato: support@meuapp.com
        - Tutorial: Clique aqui para vídeo
        """)
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

# Sidebar: Header + botões com ar
sidebar_menu = pn.Column(
    pn.pane.HTML('<h3 style="color: #1976d2; text-align: center; margin: 20px 0;">Meu App</h3>'),
    pn.layout.Divider(),
    user_btn,
    pn.layout.Spacer(height=10),
    systems_btn,
    pn.layout.Spacer(height=10),
    help_btn,
    pn.layout.Spacer(height=20),
    sizing_mode='stretch_height'
)

# Template: Sidebar menu, main reativo
template = pn.template.MaterialTemplate(
    title="Dashboard Moderno",
    sidebar=[sidebar_menu],
    main=[main_content],  # Agora bindado, sem erro
)

template.servable()