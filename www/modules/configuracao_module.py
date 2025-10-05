# modules/configuracao_module.py
import panel as pn

def get_content():
    return pn.Column(
        pn.pane.Markdown("## ⚙️ Configurações Gerais"),
        pn.layout.Divider(),
        pn.Row(
            pn.Column(
                pn.pane.Markdown("### Preferências de UI"),
                pn.widgets.Select(name="Tema", options=['Claro', 'Escuro', 'Automático'], width=200),
                pn.widgets.Select(name="Idioma", options=['Português', 'English', 'Español'], width=200),
                pn.widgets.Switch(name="Sidebar Rebatível", value=True),
                pn.widgets.Switch(name="Modo Compacto", value=False),
            ),
            pn.Column(
                pn.pane.Markdown("### Notificações"),
                pn.widgets.Switch(name="Notificações por Email", value=True),
                pn.widgets.Switch(name="Notificações Push", value=True),
                pn.widgets.Select(name="Frequência", options=['Imediato', 'Diário', 'Semanal'], width=200),
            )
        ),
        pn.layout.Divider(),
        pn.Row(
            pn.widgets.Button(name="💾 Salvar Configurações", button_type="success"),
            pn.widgets.Button(name="🔄 Restaurar Padrões", button_type="warning"),
        ),
        styles={'padding': '20px'}
    )

def get_seguranca():
    return pn.Column(
        pn.pane.Markdown("## 🔐 Configurações de Segurança"),
        pn.layout.Divider(),
        pn.Row(
            pn.Column(
                pn.pane.Markdown("### Autenticação"),
                pn.widgets.Switch(name="Autenticação de Dois Fatores", value=False),
                pn.widgets.Select(name="Tempo de Sessão", options=['1 hora', '8 horas', '24 horas', '7 dias'], width=200),
                pn.widgets.PasswordInput(name="Nova Senha", placeholder="••••••••", width=200),
            ),
            pn.Column(
                pn.pane.Markdown("### Dispositivos"),
                pn.widgets.Button(name="🔐 Gerenciar Dispositivos", button_type="primary"),
                pn.widgets.Button(name="📱 Sessões Ativas", button_type="warning"),
            )
        ),
        styles={'padding': '20px'}
    )

def get_logs():
    logs_data = [
        "2024-01-15 10:30:15 - Login bem-sucedido",
        "2024-01-15 11:45:22 - Perfil atualizado", 
        "2024-01-15 14:20:33 - Relatório exportado",
        "2024-01-15 16:05:47 - Configurações modificadas"
    ]
    
    return pn.Column(
        pn.pane.Markdown("## 📋 Log de Atividades"),
        pn.layout.Divider(),
        pn.widgets.Select(name="Tipo de Log", options=['Todos', 'Login', 'Sistema', 'Segurança'], width=200),
        pn.widgets.DateRangeSlider(name="Período", width=400),
        pn.layout.Divider(),
        pn.pane.Markdown("### Últimas Atividades:"),
        *[pn.pane.Markdown(f"`{log}`") for log in logs_data],
        pn.widgets.Button(name="📥 Exportar Logs", button_type="primary"),
        styles={'padding': '20px'}
    )

def get_backup():
    return pn.Column(
        pn.pane.Markdown("## 🔄 Backup e Restauração"),
        pn.layout.Divider(),
        pn.Row(
            pn.Column(
                pn.pane.Markdown("### Backup"),
                pn.widgets.Select(name="Frequência Backup", options=['Diário', 'Semanal', 'Mensal'], width=200),
                pn.widgets.Button(name="💾 Criar Backup Agora", button_type="success"),
            ),
            pn.Column(
                pn.pane.Markdown("### Restauração"),
                pn.widgets.Select(name="Backup Disponível", options=['backup_2024_01_15', 'backup_2024_01_14'], width=200),
                pn.widgets.Button(name="🔄 Restaurar Backup", button_type="warning"),
            )
        ),
        pn.layout.Divider(),
        pn.pane.Markdown("### 📊 Status do Backup"),
        pn.pane.Markdown("""
        - **Último Backup**: 2024-01-15 02:00:00
        - **Próximo Backup**: 2024-01-16 02:00:00  
        - **Tamanho Total**: 245 MB
        - **Status**: ✅ Saudável
        """),
        styles={'padding': '20px'}
    )