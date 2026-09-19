import wx

from app.config import (
BG, BLUE, BLUE_DARK, GREEN, GREEN_BG, NAVY, NAVY_2, RED, RED_BG,
TEXT, MUTED, WHITE, YELLOW, YELLOW_BG,
)

from app.ui.animations import animate_gauge
from app.ui.theme import accessible, apply_font, colour

class Header(wx.Panel):
  def __init__(self, parent):
    super().__init__(parent)
    self.SetBackgroundColour(colour(NAVY))
    self.SetMinSize((-1, 92))
    self.Bind(wx.EVT_PAINT, self.on_paint)
    self.Bind(wx.EVT_SIZE, lambda event: (self.Refresh(), event.Skip()))

    root = wx.BoxSizer(wx.HORIZONTAL)
    text = wx.BoxSizer(wx.VERTICAL)

    title = wx.StaticText(self, label="LPSGH FINANÇAS")
    apply_font(title, 19, True)
    tittle.SetForegroundColour(colour(WHITE))
    tittle.SetBackgroundColour(colour(NAVY))
    accessible(title, "Título do aplicativo LPSGH Finanças", "Título Principal")

    subtitle = wx.StaticText(self, label="Planejamento mensal simples, elegante e acessível")
    apply_font(subtitle, 10)
    subtitle.SetForegroundColour(colour((222, 236, 246)))
    subtitle.SetBackgroundColour(colour(NAVY))
    accessible(subtitle, "Descrição do aplicativo", "Descrição do aplicativo.")

    text.Add(title, 0, wx.BOTTOM, 4)
    text.Add(subtitle, 0)
    root.Add(text, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 18)

    badge = wx.StaticText(self, label="ACESSÍVEL", style=wx.ALIGN_CENTER)
    apply = font(badge, 9, True)
    badge.SetBackgroundColour(colour(WHITE))
    badge.SetForegroundColour(colour(NAVY))
    accessible(badge, "Indicação de acessibilidade", "Aplicativo preparado para teclado, NVDA e DOSVOX.")
    root.Add(badge, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 18)
    self.SetSizer(root)

    for control in (title, subtitle):
      control.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)

  def on_paint(self, event):
    width, height = self.GetSize()
    if width <= 0 or height <= 0:
      return
    dc = wx.PaintDC(self)
    gc = wx.GraphicsContext.Create(dc)
    if gc is None:
      dc.SetBackground(wx.Brush(colour(NAVY)))
      dc.Clear
      return
    brush = gc.CreateLinearGradientBrush(
      0, 0, width, height, colour(BLUE), colour(NAVY_2)
    )
    gc.SetBrush(brush)
    gc.SetPen(wx.TRANSPARENT_PEN)
    gc.DrawRectangle(0, 0, width, height)


class SectionTitle(wx.Panel):
  def __init__(self, parent, number, title, description):
    super().__init__(parent)
    self.SetBackgroundColour(colour(WHITE))
    root = wx.BoxSizer(wx.HORIZONTAL)
    number_box = wx.Panel(self)
    number_box.SetBackgroundColour(colour(BLUE))
    number_box.SetMinSize((38, 38))
    number_root = wx.BoxSizer(wx.VERTICAL)
    number_text = wx.StaticText(number_box, label=str(number), style=wx.ALIGN_CENTER)
    appy_font(number_text, 11, True)
    number_text.SetForegroundColour(colour(WHITE))
    number_root.Add(number_text, 1, wx.EXPAND | wx.ALL, 4)
    number_box.SetSizer(number_root)

    details = wx.BoxSizer(wx.VERTICAL)
    title_text = wx.StaticText(self, label=title)
    apply_font(title_text, 12, True)
    title_text.SetForegroundColour(colour(TEXT))
    accessible(title_text, f"Seção {number}: {title}", title)
    description_text = wx.StaticText(self, label=description)
    apply_font(description_text, 9)
    description_text.SetForegroundColour(colour(MUTED))
    accessible(description_text, f"Descrição da seção {title}", description)
    details.Add(title_text, 0, wx.BOTTOM, 2)
    details.Add(description_text, 0)

    root.Add(number_box, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
    root.Add(details, 1, wx.ALIGN_CENTER_VERTICAL)
    self.SetSizer(root)
    self.SetMinSize((-1, 52))


class Metric(wx.Panel):
    def __init__(self, parent, label, value):
        super().__init__(parent)
        self.SetBackgroundColour(colour(BG))
        root = wx.BoxSizer(wx.VERTICAL)
        self.label = wx.StaticText(self, label=label)
        apply_font(self.label, 9, True)
        self.label.SetForegroundColour(colour(MUTED))
        self.value = wx.StaticText(self, label=value)
        apply_font(self.value, 15, True)
        self.value.SetForegroundColour(colour(TEXT))
        accessible(self.label, f"Indicador {label}", f"Indicador: {label}.")
        accessible(self.value, f"Valor de {label}", f"Valor atual de {label}.")
        root.Add(self.label, 0, wx.BOTTOM, 4)
        root.Add(self.value, 0)
        self.SetSizer(root)
        self.SetMinSize((-1, 76))

    def set_value(self, value):
        self.value.SetLabel(value)


class ResultCard(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(colour(WHITE))
        root = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Visão geral")
        apply_font(title, 13, True)
        title.SetForegroundColour(colour(TEXT))
        accessible(title, "Visão geral financeira", "Resumo financeiro.")
        root.Add(title, 0, wx.BOTTOM, 10)

        grid = wx.GridSizer(2, 2, 8, 8)
        self.salary = Metric(self, "Salário mensal", "R$ 0,00")
        self.total = Metric(self, "Total das contas", "R$ 0,00")
        self.paid = Metric(self, "Contas pagas", "R$ 0,00")
        self.pending = Metric(self, "Contas pendentes", "R$ 0,00")
        for item in (self.salary, self.total, self.paid, self.pending):
            grid.Add(item, 1, wx.EXPAND)
        root.Add(grid, 0, wx.EXPAND | wx.BOTTOM, 10)

        balance_label = wx.StaticText(self, label="Saldo disponível")
        apply_font(balance_label, 10, True)
        balance_label.SetForegroundColour(colour(MUTED))
        self.balance = wx.StaticText(self, label="R$ 0,00")
        apply_font(self.balance, 22, True)
        self.balance.SetForegroundColour(colour(TEXT))
        accessible(balance_label, "Saldo disponível", "Saldo restante após as contas.")
        accessible(self.balance, "Valor do saldo disponível", "Saldo restante após as contas.")
        root.Add(balance_label, 0, wx.BOTTOM, 3)
        root.Add(self.balance, 0, wx.BOTTOM, 10)

        self.situation = wx.StaticText(self, label="Situação: aguardando dados.")
        apply_font(self.situation, 10, True)
        accessible(self.situation, "Situação financeira", "Mensagem textual do resultado.")
        root.Add(self.situation, 0, wx.EXPAND | wx.BOTTOM, 10)

        percent = wx.StaticText(self, label="Comprometimento do salário")
        apply_font(percent, 9, True)
        percent.SetForegroundColour(colour(MUTED))
        self.percent_value = wx.StaticText(self, label="0,00%")
        apply_font(self.percent_value, 12, True)
        self.progress = wx.Gauge(self, range=100, style=wx.GA_HORIZONTAL)
        accessible(percent, "Comprometimento do salário", "Percentual do salário usado pelas contas.")
        accessible(self.percent_value, "Percentual comprometido", "Percentual do salário usado pelas contas.")
        accessible(self.progress, "Barra de comprometimento", "Indicação visual complementar ao percentual.")
        root.Add(percent, 0, wx.BOTTOM, 3)
        root.Add(self.percent_value, 0, wx.BOTTOM, 5)
        root.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(root)

    def update(self, summary, formatter):
        # Textos definidos de imediato: leitura correta e instantânea por
        # NVDA/DOSVOX não depende da animação da barra abaixo.
        self.salary.set_value(f"R$ {formatter(summary.salary)}")
        self.total.set_value(f"R$ {formatter(summary.total)}")
        self.paid.set_value(f"R$ {formatter(summary.paid_total)}")
        self.pending.set_value(f"R$ {formatter(summary.pending_total)}")
        self.balance.SetLabel(f"R$ {formatter(summary.balance)}")
        self.percent_value.SetLabel(f"{formatter(summary.percentage)}%")

        # Só a barra visual anima suavemente até o novo percentual.
        animate_gauge(self.progress, int(summary.percentage))

        if summary.balance > 0:
            text = "Situação positiva. Existe saldo disponível depois das contas."
            self.situation.SetForegroundColour(colour(GREEN))
            self.situation.SetBackgroundColour(colour(GREEN_BG))
            self.SetBackgroundColour(colour(GREEN_BG))
        elif summary.balance < 0:
            text = f"Situação de atenção. Faltam R$ {formatter(abs(summary.balance))}."
            self.situation.SetForegroundColour(colour(RED))
            self.situation.SetBackgroundColour(colour(RED_BG))
            self.SetBackgroundColour(colour(RED_BG))
        else:
            text = "Situação equilibrada. As contas consomem exatamente o salário."
            self.situation.SetForegroundColour(colour(YELLOW))
            self.situation.SetBackgroundColour(colour(YELLOW_BG))
            self.SetBackgroundColour(colour(YELLOW_BG))
        self.situation.SetLabel(text)
        self.Layout()
