# Sistema de Match Entre Desenvolvedores e Empresas

## Objetivo do Sistema

O objetivo deste sistema é permitir que **desenvolvedores** e **empresas** se conectem de forma eficiente através de uma plataforma de busca e match. O sistema permite que ambos os lados se registrem, façam login, visualizem perfis e indiquem interesse, com o objetivo de gerar uma correspondência ("match") quando ambos expressam interesse mútuo.

## Requisitos Principais

1. **Sistema de Registro e Login** para desenvolvedores e empresas.
2. **Mecanismo de busca de perfis**, permitindo que desenvolvedores busquem empresas e vice-versa.
3. **Funcionalidade de Match**, onde ambas as partes podem indicar interesse mútuo.
4. **Listagem de novos matches confirmados**.
5. **Possibilidade de cancelamento de matches**.
6. **Autenticação segura** para garantir a integridade e a privacidade dos usuários.
   
## Como Rodar
1. git clone https://github.com/seu-usuario/tinder_job_dcc603.git
2. cd tinder_job_dcc603/TINDERJOB
3. Utilizar python 3.12.
4. No Linux utilize source .venv/bin/activate
5. pip install -r requirements.txt
6. Utilize python3.12 main.py

## Bibliotecas Necessárias

Certifique-se de ter as seguintes bibliotecas instaladas para o funcionamento do sistema:

```bash
Flask==2.3.2
Flask-Bootstrap==5.3.0
Flask-WTF==1.2.1
WTForms==3.0.1
Flask-SQLAlchemy==2.5.1
Werkzeug==3.0.0

