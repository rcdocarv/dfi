import panel as pn

def get_systems_content():
    return pn.pane.Markdown("""
    # Sistemas
    
    Gerencie os sistemas disponíveis.
    
    - Sistema A: Status online
    - Sistema B: Manutenção em andamento
    - Sistema C: Offline
    """)