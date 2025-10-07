import panel as pn

def get_help_content():
    return pn.pane.Markdown("""
    # Ajuda
    
    Precisa de suporte? Consulte nossa documentação.
    
    - FAQ: Perguntas frequentes
    - Contato: support@meuapp.com
    - Tutorial: Clique aqui para vídeo
    """)