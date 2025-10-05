# modules/dashboard.py
import panel as pn
import asyncio
from auth_manager import AuthManager

class DashboardModule:
    def __init__(self, auth_manager):
        self.auth = auth_manager
        self.main_content = pn.Column()
        
        # Importar outros módulos
        from modules.perfil import PerfilModule
        from modules.relatorios import RelatoriosModule
        from modules.configuracao import ConfiguracaoModule
        
        self.perfil_module = PerfilModule(auth_manager)
        self.relatorios_module = RelatoriosModule(auth_manager)
        self.configuracao_module = ConfiguracaoModule(auth_manager)
        
        # Mostrar perfil por padrão
        self.show_module('perfil')
    
    def create_sidebar(self):
        """Cria a sidebar collapsible do dashboard"""
        sidebar_content = pn.Column(
            pn.pane.Markdown("## 🎯 Navegação"),
            pn.layout.Divider(),
            pn.widgets.Button(name="🏠 Dashboard", button_type="primary", width=200),
            pn.widgets.Button(name="👤 Meu Perfil", button_type="primary", width=200),
            pn.widgets.Button(name="📊 Relatórios", button_type="primary", width=200),
            pn.widgets.Button(name="⚙️ Configurações", button_type="primary", width=200),
            pn.layout.Divider(),
            pn.widgets.Button(name="🚪 Logout", button_type="warning", width=200),
            styles={'padding': '20px'}
        )
        
        # Configurar callbacks
        sidebar_content[2].on_click(lambda e: self.show_module('dashboard'))
        sidebar_content[3].on_click(lambda e: self.show_module('perfil'))
        sidebar_content[4].on_click(lambda e: self.show_module('relatorios'))
        sidebar_content[5].on_click(lambda e: self.show_module('configuracao'))
        sidebar_content[7].on_click(lambda e: asyncio.create_task(self.logout_callback(e)))
        
        return sidebar_content
    
    def show_module(self, module_name):
        """Mostra o módulo selecionado no conteúdo principal"""
        if module_name == 'dashboard':
            self.main_content.objects = [self.get_dashboard_content()]
        elif module_name == 'perfil':
            self.main_content.objects = [self.perfil_module.view()]
        elif module_name == 'relatorios':
            self.main_content.objects = [self.relatorios_module.view()]
        elif module_name == 'configuracao':
            self.main_content.objects = [self.configuracao_module.view()]
    
    def get_dashboard_content(self):
        """Conteúdo principal do dashboard"""
        return pn.Column(
            pn.pane.Markdown(f"# 🎉 Bem-vindo, {self.auth.current_user}!"),
            pn.layout.Divider(),
            pn.pane.Markdown("""
            ### 📈 Visão Geral do Sistema
            
            **Estatísticas Rápidas:**
            - ✅ Usuários ativos: 1
            - 📊 Relatórios gerados: 0
            - ⚙️ Configurações disponíveis: 3
            
            **Ações Rápidas:**
            - Acesse seu **Perfil** para atualizar informações
            - Gere **Relatórios** personalizados
            - Configure o sistema em **Configurações**
            """),
            styles={'padding': '20px'}
        )
    
    async def logout_callback(self, event):
        """Callback para logout"""
        success, msg = await self.auth.logout_user()
        # A mensagem será mostrada no login_view através do parâmetro message
    
    def view(self):
        """Retorna a view completa do dashboard"""
        return pn.Column(
            self.main_content,
            sizing_mode="stretch_width"
        )