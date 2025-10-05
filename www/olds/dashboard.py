import panel as pn

def dashboard_view(auth, logout_btn):
    return pn.Column(
        pn.pane.Markdown(f"# 🎉 Bem-vindo, {auth.current_user}!"),
        pn.pane.Markdown("### Você está logado no sistema"),
        pn.layout.Divider(),
        pn.widgets.Button(name="Meu Perfil", button_type="primary"),
        pn.widgets.Button(name="Configurações", button_type="primary"),
        logout_btn,
        sizing_mode="stretch_width",
    )
