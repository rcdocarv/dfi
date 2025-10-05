# modules/relatorios.py
import panel as pn
import pandas as pd
from datetime import datetime, timedelta

class RelatoriosModule:
    def __init__(self, auth_manager):
        self.auth = auth_manager
    
    def view(self):
        # Dados de exemplo
        data = {
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'Vendas (€)': [12000, 15000, 18000, 9000, 20000, 17000],
            'Crescimento (%)': [5, 8, 12, -5, 15, 10]
        }
        df = pd.DataFrame(data)
        
        return pn.Column(
            pn.pane.Markdown("## 📊 Relatórios de Vendas"),
            pn.layout.Divider(),
            pn.Row(
                pn.Column(
                    pn.pane.Markdown("### Dados Mensais"),
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
                )
            ),
            styles={'padding': '20px'}
        )