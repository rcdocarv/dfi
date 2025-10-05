# modules/configuracao.py
import panel as pn

class ConfiguracaoModule:
    def __init__(self, auth_manager):
        self.auth = auth_manager
    
    def view(self):
        return pn.Column(
            pn.pane.Markdown("## ⚙️ Configurações do Sistema"),
            pn.layout.Divider(),
            pn.Row(
                pn.Column(
                    pn.pane.Markdown("### Preferências"),
                    pn.widgets.Select(name="Tema", options=['Claro', 'Escuro', 'Automático'], width=200),
                    pn.widgets.Select(name="Idioma", options=['Português', 'English', 'Español'], width=200),
                    pn.widgets.Switch(name="Notificações por Email", value=True),
                ),
                pn.Column(
                    pn.pane.Markdown("### Segurança"),
                    pn.widgets.Switch(name="Autenticação de Dois Fatores", value=False),
                    pn.widgets.Select(name="Tempo de Sessão", options=['1 hora', '8 horas', '24 horas', '7 dias'], width=200),
                )
            ),
            pn.layout.Divider(),
            pn.Row(
                pn.widgets.Button(name="💾 Salvar Configurações", button_type="success"),
                pn.widgets.Button(name="🔄 Restaurar Padrões", button_type="warning"),
            ),
            styles={'padding': '20px'}
        )