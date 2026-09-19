import wx

from app.config import APP_NAME, APP_VERSION, SHORTCUTS, WHITE
from app.ui.theme import accessible, apply_font, colour, button_style


class HelpDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Ajuda e acessibilidade", size=(900, 740), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetBackgroundColour(colour(WHITE))
        root = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, label="AJUDA, TECLADO E ACESSIBILIDADE")
        apply_font(title, 16, True)
        title.SetForegroundColour(colour((15, 28, 40)))
        accessible(title, "Título da ajuda", "Manual de uso e acessibilidade.")

        intro = wx.StaticText(self, label="O programa foi organizado para uso por teclado, com controles nativos e informações em texto.")
        apply_font(intro, 10)

        text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        apply_font(text, 10)
        text.SetValue(self.content())
        accessible(text, "Manual de acessibilidade", "Use as setas para ler o conteúdo.")

        close = wx.Button(self, label="Fechar")
        button_style(close, primary=True)
        accessible(close, "Fechar ajuda", "Fecha a janela de ajuda.")
        close.Bind(wx.EVT_BUTTON, lambda event: self.EndModal(wx.ID_OK))

        root.Add(title, 0, wx.ALL, 16)
        root.Add(intro, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 16)
        root.Add(text, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 16)
        root.Add(close, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 16)
        self.SetSizer(root)
        self.CentreOnParent()
        text.SetFocus()

    @staticmethod
    def content():
        lines = [
            f"{APP_NAME} - versão {APP_VERSION}",
            "",
            "OBJETIVO",
            "",
            "Informe o salário, cadastre as contas e acompanhe o saldo mensal.",
            "",
            "NAVEGAÇÃO",
            "",
            "TAB: próximo controle.",
            "SHIFT + TAB: controle anterior.",
            "ENTER: ativa botões e confirma ações.",
            "ESC: fecha diálogos quando disponível.",
            "SETA PARA CIMA E SETA PARA BAIXO: navegam em listas e categorias.",
            "",
            "ATALHOS",
            "",
        ]
        lines.extend(f"{key}: {description}." for key, description in SHORTCUTS)
        lines.extend([
            "",
            "ATENÇÃO: F4 leva ao cadastro da conta; F6 remove a conta selecionada; F7 altera paga ou pendente.",
            "",
            "NVDA",
            "",
            "O aplicativo usa controles nativos do wxPython, rótulos claros, nomes de controles e foco previsível.",
            "Com o NVDA ativo, use TAB e SHIFT + TAB para percorrer a interface. A lista de contas usa as setas.",
            "As informações importantes também aparecem em texto e não dependem somente de cores.",
            "As pequenas animações visuais (realce de botões e barra de progresso) são só decorativas: os",
            "valores lidos pelo leitor de tela são sempre atualizados de forma imediata, sem esperar a animação.",
            "",
            "DOSVOX",
            "",
            "A navegação principal pode ser feita sem mouse usando TAB, SHIFT + TAB, ENTER e as setas.",
            "As mensagens de resultado são textuais para permitir leitura pela fala.",
            "",
            "SEM TRAVAMENTO",
            "",
            "O aplicativo é local e não executa consultas de rede. Os cálculos são leves e imediatos.",
            "Operações maiores devem permanecer fora do fluxo principal da interface para preservar a responsividade.",
            "",
            "SALVAMENTO",
            "",
            "Ctrl+S salva os dados localmente. Ctrl+O carrega. Ctrl+E exporta as contas em CSV.",
            "",
            "TESTE RECOMENDADO",
            "",
            "Faça todo o processo apenas com teclado e com o leitor de tela ativo: salário, conta, seleção, paga, cálculo, salvar, carregar e ajuda.",
            "",
            "A experiência final pode variar conforme Windows, wxPython, NVDA, DOSVOX e configurações de acessibilidade.",
        ])
        return "\n".join(lines)
