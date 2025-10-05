# modules/perfil_module.py
import panel as pn
import pandas as pd
from datetime import datetime

def get_content(username):
    return pn.Column(
        pn.pane.Markdown("## 👤 Meu Perfil - Informações Pessoais"),
        pn.layout.Divider(),
        pn.widgets.TextInput(name="Nome Completo", value=username, width=300),
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

def get_estatisticas(username):
    data = {
        'Métrica': ['Projetos Concluídos', 'Tarefas Pendentes', 'Horas Trabalhadas', 'Feedback Positivo'],
        'Valor': [15, 8, '120h', '95%']
    }
    df = pd.DataFrame(data)
    
    return pn.Column(
        pn.pane.Markdown("## 📈 Minhas Estatísticas"),
        pn.layout.Divider(),
        pn.widgets.DataFrame(df, width=400),
        pn.pane.Markdown("""
        ### 📊 Desempenho Mensal
        - **Produtividade**: 85%
        - **Pontualidade**: 92%
        - **Qualidade**: 88%
        """),
        pn.widgets.Button(name="📥 Exportar Relatório", button_type="primary"),
        styles={'padding': '20px'}
    )

def get_metas(username):
    return pn.Column(
        pn.pane.Markdown("## 🎯 Minhas Metas e Objetivos"),
        pn.layout.Divider(),
        pn.widgets.TextInput(name="Meta Trimestral", placeholder="Aumentar produtividade em 15%", width=400),
        pn.widgets.TextInput(name="Prazo", value=datetime.now().strftime("%Y-%m-%d"), width=200),
        pn.widgets.Select(name="Prioridade", options=['Alta', 'Média', 'Baixa'], width=200),
        pn.layout.Divider(),
        pn.pane.Markdown("### Metas em Andamento:"),
        pn.widgets.Checkbox(name="Concluir treinamento Python", value=False),
        pn.widgets.Checkbox(name="Implementar novo módulo", value=True),
        pn.widgets.Checkbox(name="Documentar processos", value=False),
        pn.widgets.Button(name="🎯 Adicionar Nova Meta", button_type="success"),
        styles={'padding': '20px'}
    )