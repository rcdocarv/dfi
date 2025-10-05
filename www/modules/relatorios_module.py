# modules/relatorios_module.py
import panel as pn
import pandas as pd
from datetime import datetime, timedelta

def get_content(tipo='vendas'):
    if tipo == 'vendas':
        data = {
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'Vendas (€)': [12000, 15000, 18000, 9000, 20000, 17000],
            'Crescimento (%)': [5, 8, 12, -5, 15, 10]
        }
        titulo = "Vendas"
    elif tipo == 'usuarios':
        data = {
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'Novos Usuários': [50, 75, 100, 60, 120, 110],
            'Usuários Ativos': [200, 220, 250, 230, 300, 280]
        }
        titulo = "Usuários"
    elif tipo == 'financeiro':
        data = {
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'Receita (€)': [10000, 12000, 15000, 8000, 20000, 17000],
            'Despesas (€)': [5000, 6000, 7000, 4000, 9000, 8000]
        }
        titulo = "Financeiro"
    elif tipo == 'marketing':
        data = {
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'Leads': [150, 180, 200, 120, 250, 220],
            'Conversão (%)': [12, 15, 18, 10, 20, 17]
        }
        titulo = "Marketing"
    
    df = pd.DataFrame(data)
    
    return pn.Column(
        pn.pane.Markdown(f"## 📊 Relatórios - {titulo}"),
        pn.layout.Divider(),
        pn.Row(
            pn.Column(
                pn.pane.Markdown("### Dados Detalhados"),
                pn.widgets.DataFrame(df, width=500, height=200),
                pn.widgets.DateRangeSlider(
                    name="Período", 
                    value=(datetime.now() - timedelta(days=90), datetime.now()),
                    width=400
                ),
            ),
            pn.Column(
                pn.pane.Markdown("### Ações"),
                pn.widgets.Select(
                    name="Formato Exportação", 
                    options=['PDF', 'Excel', 'CSV', 'HTML'],
                    width=200
                ),
                pn.widgets.Button(name="📥 Exportar Relatório", button_type="primary"),
                pn.widgets.Button(name="🔄 Atualizar Dados", button_type="success"),
                pn.widgets.Button(name="📊 Gerar Gráfico", button_type="warning"),
            )
        ),
        pn.layout.Divider(),
        pn.pane.Markdown(f"### 📈 Resumo {titulo}"),
        pn.pane.Markdown(f"""
        - **Total**: {df[df.columns[1]].sum() if df.columns[1] != 'Crescimento (%)' else f"{df[df.columns[1]].mean():.1f}%"}
        - **Média Mensal**: {df[df.columns[1]].mean():.0f if df.columns[1] != 'Crescimento (%)' else f"{df[df.columns[1]].mean():.1f}%"}
        - **Melhor Mês**: {df.loc[df[df.columns[1]].idxmax(), 'Mês']}
        - **Tendência**: {'📈 Positiva' if df[df.columns[1]].iloc[-1] > df[df.columns[1]].iloc[0] else '📉 Negativa'}
        """),
        styles={'padding': '20px'}
    )