import panel as pn

def get_user_content(current_user):
    return pn.pane.Markdown(f"""
    # Perfil do Usuário
    
    Bem-vindo ao seu perfil, {current_user}!
    
    - Nome: João Silva
    - Email: joao@email.com
    - Último login: 05/10/2025
    """)