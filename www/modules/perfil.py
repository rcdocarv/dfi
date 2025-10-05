# modules/perfil.py
import panel as pn

class PerfilModule:
    def __init__(self, auth_manager):
        self.auth = auth_manager
    
    def view(self):
        return pn.Column(
            pn.pane.Markdown("## 👤 Meu Perfil"),
            pn.layout.Divider(),
            pn.widgets.TextInput(name="Nome de Usuário", value=self.auth.current_user, width=300, disabled=True),
            pn.widgets.TextInput(name="Email", placeholder="seu@email.com", width=300),
            pn.widgets.TextInput(name="Telefone", placeholder="+351 123 456 789", width=300),
            pn.widgets.TextInput(name="Departamento", placeholder="TI", width=300),
            pn.layout.Divider(),
            pn.Row(
                pn.widgets.Button(name="💾 Salvar Alterações", button_type="primary"),
                pn.widgets.Button(name="🔒 Alterar Senha", button_type="warning"),
            ),
            styles={'padding': '20px'}
        )