"""
Gera o executável do LPSGH Financas usando o PyInstaller.

Como usar (no Windows, dentro da pasta do projeto):
    python -m pip install -r requirements.txt
    python build_installer.py

Ao final, o executável fica em:
    dist/LPSGH_Financas/LPSGH_Financas.exe

Esse .exe (ou a pasta "dist/LPSGH_Financas" inteira) já pode ser copiado para
outro computador e executado diretamente. O passo seguinte (opcional) é usar
o Inno Setup com o arquivo installer/lpsgh_financas.iss para transformar essa
pasta em um instalador único (um arquivo "LPSGH_Financas_Setup.exe" que
instala o programa com atalho no menu iniciar e ícone na área de trabalho).
"""

import PyInstaller.__main__

APP_NAME = "LPSGH_Financas"

PyInstaller.__main__.run([
    "main.py",
    f"--name={APP_NAME}",
    "--windowed",       # não abre janela de console junto com o programa
    "--onedir",         # gera uma pasta com o .exe e as dependências
    "--noconfirm",
    "--clean",
    # Se você adicionar um ícone próprio (arquivo .ico) na raiz do projeto,
    # descomente a linha abaixo trocando "icone.ico" pelo nome do arquivo:
    # "--icon=icone.ico",
])

print("\nPronto! O executável está em: dist/" + APP_NAME + "/" + APP_NAME + ".exe")
