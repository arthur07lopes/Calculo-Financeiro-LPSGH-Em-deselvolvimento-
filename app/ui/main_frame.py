import wx

from app.config import APP_NAME, BG, CATEGORIES, MIN_SIZE, NAVY_2, TEXT, WHITE, BLUE, RED
from app.core.finance import FinanceManager, format_money, parse_money
from app.services.storage import StorageService
from app.ui.animations import fade_in_window
from app.ui.components import Header, SectionTitle, ResultCard
from app.ui.dialogs import HelpDialog
from app.ui.theme import accessible, apply_font, button_style, colour


class MainFrame(wx.Frame):
    def __init__(self, storage, title, size, min_size):
        super().__init__(None, title=title, size=size, style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetMinSize(min_size)
        self.SetBackgroundColour(colour(BG))
        self.manager = FinanceManager()
        self.storage = storage
        self.create_menu()
        self.create_interface()
        self.create_shortcuts()
        self.create_status()
        self.bind_events()
        self.update_ui()
        accessible(self, APP_NAME, "Calculadora financeira. Pressione F1 para ajuda.")

    def create_menu(self):
        bar = wx.MenuBar()
        file_menu = wx.Menu()
        self.mi_new = file_menu.Append(wx.ID_NEW, "Nova análise\tCtrl+N")
        self.mi_save = file_menu.Append(wx.ID_SAVE, "Salvar análise\tCtrl+S")
        self.mi_load = file_menu.Append(wx.ID_OPEN, "Carregar análise\tCtrl+O")
        self.mi_export = file_menu.Append(wx.ID_ANY, "Exportar CSV\tCtrl+E")
        file_menu.AppendSeparator()
        self.mi_exit = file_menu.Append(wx.ID_EXIT, "Sair\tCtrl+Q")

        action_menu = wx.Menu()
        self.mi_calc = action_menu.Append(wx.ID_ANY, "Atualizar cálculo\tF3")
        self.mi_add = action_menu.Append(wx.ID_ANY, "Ir para cadastro\tF4")
        self.mi_remove = action_menu.Append(wx.ID_ANY, "Remover selecionada\tF6")
        self.mi_paid = action_menu.Append(wx.ID_ANY, "Marcar ou desmarcar paga\tF7")

        help_menu = wx.Menu()
        self.mi_help = help_menu.Append(wx.ID_HELP, "Ajuda e acessibilidade\tF1")
        self.mi_about = help_menu.Append(wx.ID_ABOUT, "Sobre")

        bar.Append(file_menu, "Arquivo")
        bar.Append(action_menu, "Ações")
        bar.Append(help_menu, "Ajuda")
        self.SetMenuBar(bar)

    def create_interface(self):
        root = wx.BoxSizer(wx.VERTICAL)
        root.Add(Header(self), 0, wx.EXPAND)

        self.scroll = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scroll.SetScrollRate(10, 10)
        self.scroll.SetBackgroundColour(colour(BG))
        content = wx.BoxSizer(wx.VERTICAL)

        salary = wx.Panel(self.scroll)
        salary.SetBackgroundColour(colour(WHITE))
        salary_root = wx.BoxSizer(wx.VERTICAL)
        salary_root.Add(SectionTitle(salary, "1", "Salário mensal", "Informe o valor líquido usado no planejamento."), 0, wx.EXPAND | wx.ALL, 14)
        salary_row = wx.BoxSizer(wx.HORIZONTAL)
        salary_box = wx.BoxSizer(wx.VERTICAL)
        salary_label = wx.StaticText(salary, label="Valor do salário")
        apply_font(salary_label, 9, True)
        self.salary = wx.TextCtrl(salary, style=wx.TE_PROCESS_ENTER, size=(250, -1))
        self.salary.SetHint("Exemplo: 3000,00")
        accessible(self.salary, "Salário mensal", "Digite o salário líquido mensal em reais.")
        salary_box.Add(salary_label, 0, wx.BOTTOM, 4)
        salary_box.Add(self.salary, 0)
        salary_row.Add(salary_box, 0, wx.RIGHT, 12)
        self.apply_salary = wx.Button(salary, label="Aplicar salário")
        button_style(self.apply_salary, primary=True)
        accessible(self.apply_salary, "Aplicar salário", "Aplica o salário ao cálculo.")
        salary_row.Add(self.apply_salary, 0, wx.ALIGN_BOTTOM)
        salary_root.Add(salary_row, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)
        salary.SetSizer(salary_root)
        content.Add(salary, 0, wx.ALL | wx.EXPAND, 16)

        main = wx.BoxSizer(wx.HORIZONTAL)
        left = wx.Panel(self.scroll)
        left.SetBackgroundColour(colour(WHITE))
        left_root = wx.BoxSizer(wx.VERTICAL)
        left_root.Add(SectionTitle(left, "2", "Contas mensais", "Cadastre despesas e acompanhe o estado de pagamento."), 0, wx.EXPAND | wx.ALL, 14)
        form_row = wx.BoxSizer(wx.HORIZONTAL)

        form = wx.Panel(left)
        form.SetBackgroundColour(colour(WHITE))
        form_root = wx.BoxSizer(wx.VERTICAL)
        name_label = wx.StaticText(form, label="Nome da conta")
        apply_font(name_label, 9, True)
        self.account_name = wx.TextCtrl(form)
        self.account_name.SetHint("Exemplo: aluguel")
        accessible(self.account_name, "Nome da conta", "Digite o nome da conta.")
        category_label = wx.StaticText(form, label="Categoria")
        apply_font(category_label, 9, True)
        self.category = wx.ComboBox(form, choices=CATEGORIES, value="Outros")
        accessible(self.category, "Categoria da conta", "Selecione uma categoria usando as setas.")
        value_label = wx.StaticText(form, label="Valor da conta")
        apply_font(value_label, 9, True)
        self.account_value = wx.TextCtrl(form, style=wx.TE_PROCESS_ENTER)
        self.account_value.SetHint("Exemplo: 850,00")
        accessible(self.account_value, "Valor da conta", "Digite o valor da conta em reais.")
        self.add = wx.Button(form, label="Adicionar conta")
        button_style(self.add, primary=True)
        accessible(self.add, "Adicionar conta", "Adiciona a conta à lista.")
        form_root.Add(name_label, 0, wx.BOTTOM, 4)
        form_root.Add(self.account_name, 0, wx.EXPAND | wx.BOTTOM, 10)
        form_root.Add(category_label, 0, wx.BOTTOM, 4)
        form_root.Add(self.category, 0, wx.EXPAND | wx.BOTTOM, 10)
        form_root.Add(value_label, 0, wx.BOTTOM, 4)
        form_root.Add(self.account_value, 0, wx.EXPAND | wx.BOTTOM, 12)
        form_root.Add(self.add, 0, wx.EXPAND)
        form.SetSizer(form_root)
        form_row.Add(form, 1, wx.RIGHT | wx.EXPAND, 14)

        list_panel = wx.Panel(left)
        list_panel.SetBackgroundColour(colour(WHITE))
        list_root = wx.BoxSizer(wx.VERTICAL)
        list_label = wx.StaticText(list_panel, label="Contas cadastradas")
        apply_font(list_label, 10, True)
        self.accounts = wx.ListBox(list_panel, style=wx.LB_SINGLE)
        accessible(self.accounts, "Lista de contas cadastradas", "Use as setas para navegar pelas contas.")
        list_root.Add(list_label, 0, wx.BOTTOM, 6)
        list_root.Add(self.accounts, 1, wx.EXPAND | wx.BOTTOM, 10)
        list_actions = wx.BoxSizer(wx.HORIZONTAL)
        self.toggle = wx.Button(list_panel, label="Marcar paga")
        self.remove = wx.Button(list_panel, label="Remover")
        button_style(self.toggle)
        button_style(self.remove, danger=True)
        accessible(self.toggle, "Marcar ou desmarcar paga", "Alterna a situação da conta selecionada.")
        accessible(self.remove, "Remover conta", "Remove a conta selecionada.")
        list_actions.Add(self.toggle, 1, wx.RIGHT, 6)
        list_actions.Add(self.remove, 1)
        list_root.Add(list_actions, 0, wx.EXPAND)
        list_panel.SetSizer(list_root)
        form_row.Add(list_panel, 2, wx.EXPAND)
        left_root.Add(form_row, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 14)
        left.SetSizer(left_root)

        right = wx.Panel(self.scroll)
        right.SetBackgroundColour(colour(WHITE))
        right_root = wx.BoxSizer(wx.VERTICAL)
        right_root.Add(SectionTitle(right, "3", "Resumo financeiro", "Acompanhe os principais indicadores do mês."), 0, wx.EXPAND | wx.ALL, 14)
        self.result = ResultCard(right)
        self.refresh = wx.Button(right, label="Atualizar cálculo")
        button_style(self.refresh, primary=True)
        accessible(self.refresh, "Atualizar cálculo", "Recalcula o resumo financeiro.")
        right_root.Add(self.result, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 14)
        right_root.Add(self.refresh, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 14)
        right.SetSizer(right_root)

        main.Add(left, 3, wx.RIGHT | wx.EXPAND, 8)
        main.Add(right, 2, wx.EXPAND)
        content.Add(main, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 16)

        bottom = wx.Panel(self.scroll)
        bottom.SetBackgroundColour(colour(WHITE))
        bottom_root = wx.BoxSizer(wx.HORIZONTAL)
        self.save = wx.Button(bottom, label="Salvar")
        self.load = wx.Button(bottom, label="Carregar")
        self.export = wx.Button(bottom, label="Exportar CSV")
        self.new = wx.Button(bottom, label="Nova análise")
        self.help = wx.Button(bottom, label="Ajuda")
        for button in (self.save, self.load, self.export, self.new):
            button_style(button)
        button_style(self.help, primary=True)
        accessible(self.save, "Salvar análise", "Salva os dados financeiros.")
        accessible(self.load, "Carregar análise", "Carrega os dados salvos.")
        accessible(self.export, "Exportar CSV", "Exporta as contas para CSV.")
        accessible(self.new, "Nova análise", "Limpa os dados atuais.")
        accessible(self.help, "Ajuda e acessibilidade", "Abre a documentação de teclado, NVDA e DOSVOX.")
        for i, button in enumerate((self.save, self.load, self.export, self.new, self.help)):
            bottom_root.Add(button, 1, wx.RIGHT if i < 4 else 0, 6)
        bottom.SetSizer(bottom_root)
        content.Add(bottom, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 16)
        self.scroll.SetSizer(content)
        self.scroll.FitInside()
        root.Add(self.scroll, 1, wx.EXPAND)

        footer = wx.Panel(self)
        footer.SetBackgroundColour(colour(NAVY_2))
        footer_root = wx.BoxSizer(wx.HORIZONTAL)
        self.status = wx.StaticText(footer, label="Pronto.")
        apply_font(self.status, 9, True)
        self.status.SetForegroundColour(colour(WHITE))
        accessible(self.status, "Status do aplicativo", "Mensagem de status.")
        footer_text = wx.StaticText(footer, label="F1 Ajuda | F3 Calcular | F4 Cadastro | F6 Remover | F7 Paga")
        footer_text.SetForegroundColour(colour((198, 213, 225)))
        apply_font(footer_text, 8)
        footer_root.Add(self.status, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 9)
        footer_root.Add(footer_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 9)
        footer.SetSizer(footer_root)
        root.Add(footer, 0, wx.EXPAND)
        self.SetSizer(root)

    def create_shortcuts(self):
        mapping = {}
        for key in ("new", "save", "load", "export", "exit", "help", "calc", "add", "remove", "paid"):
            mapping[key] = wx.NewIdRef()

        handlers = {
            "new": self.on_new,
            "save": self.on_save,
            "load": self.on_load,
            "export": self.on_export,
            "exit": self.on_exit,
            "help": self.on_help,
            "calc": self.on_calculate,
            "add": self.on_focus_add,
            "remove": self.on_remove,
            "paid": self.on_toggle_paid,
        }
        for key, identifier in mapping.items():
            self.Bind(wx.EVT_MENU, handlers[key], id=identifier)

        entries = [
            (wx.ACCEL_CTRL, ord("N"), mapping["new"]),
            (wx.ACCEL_CTRL, ord("S"), mapping["save"]),
            (wx.ACCEL_CTRL, ord("O"), mapping["load"]),
            (wx.ACCEL_CTRL, ord("E"), mapping["export"]),
            (wx.ACCEL_CTRL, ord("Q"), mapping["exit"]),
            (wx.ACCEL_NORMAL, wx.WXK_F1, mapping["help"]),
            (wx.ACCEL_NORMAL, wx.WXK_F3, mapping["calc"]),
            (wx.ACCEL_NORMAL, wx.WXK_F4, mapping["add"]),
            (wx.ACCEL_NORMAL, wx.WXK_F6, mapping["remove"]),
            (wx.ACCEL_NORMAL, wx.WXK_F7, mapping["paid"]),
        ]
        self.SetAcceleratorTable(wx.AcceleratorTable([
            wx.AcceleratorEntry(mod, key, identifier) for mod, key, identifier in entries
        ]))

    def create_status(self):
        self.status_bar = self.CreateStatusBar(1)
        self.status_bar.SetStatusText("Pronto. Pressione F1 para ajuda.")

    def bind_events(self):
        self.apply_salary.Bind(wx.EVT_BUTTON, self.on_apply_salary)
        self.salary.Bind(wx.EVT_TEXT_ENTER, self.on_apply_salary)
        self.add.Bind(wx.EVT_BUTTON, self.on_add)
        self.account_value.Bind(wx.EVT_TEXT_ENTER, self.on_add)
        self.accounts.Bind(wx.EVT_LISTBOX, self.on_selection)
        self.toggle.Bind(wx.EVT_BUTTON, self.on_toggle_paid)
        self.remove.Bind(wx.EVT_BUTTON, self.on_remove)
        self.refresh.Bind(wx.EVT_BUTTON, self.on_calculate)
        self.save.Bind(wx.EVT_BUTTON, self.on_save)
        self.load.Bind(wx.EVT_BUTTON, self.on_load)
        self.export.Bind(wx.EVT_BUTTON, self.on_export)
        self.new.Bind(wx.EVT_BUTTON, self.on_new)
        self.help.Bind(wx.EVT_BUTTON, self.on_help)
        self.Bind(wx.EVT_MENU, self.on_new, self.mi_new)
        self.Bind(wx.EVT_MENU, self.on_save, self.mi_save)
        self.Bind(wx.EVT_MENU, self.on_load, self.mi_load)
        self.Bind(wx.EVT_MENU, self.on_export, self.mi_export)
        self.Bind(wx.EVT_MENU, self.on_exit, self.mi_exit)
        self.Bind(wx.EVT_MENU, self.on_calculate, self.mi_calc)
        self.Bind(wx.EVT_MENU, self.on_focus_add, self.mi_add)
        self.Bind(wx.EVT_MENU, self.on_remove, self.mi_remove)
        self.Bind(wx.EVT_MENU, self.on_toggle_paid, self.mi_paid)
        self.Bind(wx.EVT_MENU, self.on_help, self.mi_help)
        self.Bind(wx.EVT_MENU, self.on_about, self.mi_about)

    def on_apply_salary(self, event):
        try:
            value = parse_money(self.salary.GetValue())
            self.manager.set_salary(value)
            self.update_ui()
            self.set_status(f"Salário aplicado: R$ {format_money(value)}.")
            self.account_name.SetFocus()
        except ValueError as error:
            self.error(str(error), self.salary)
        event.Skip()

    def on_add(self, event):
        try:
            value = parse_money(self.account_value.GetValue())
            name = self.account_name.GetValue()
            self.manager.add_account(name, value, self.category.GetValue())
            clean_name = name.strip()
            self.account_name.Clear()
            self.account_value.Clear()
            self.category.SetValue("Outros")
            self.update_ui()
            self.set_status(f"Conta {clean_name} adicionada: R$ {format_money(value)}.")
            self.account_name.SetFocus()
        except ValueError as error:
            focus = self.account_name if not self.account_name.GetValue().strip() else self.account_value
            self.error(str(error), focus)
        event.Skip()

    def selected_index(self):
        return self.accounts.GetSelection()

    def on_selection(self, event):
        index = event.GetSelection()
        if index != wx.NOT_FOUND and index < len(self.manager.accounts):
            account = self.manager.accounts[index]
            self.toggle.SetLabel("Marcar pendente" if account.paid else "Marcar paga")
        event.Skip()

    def on_remove(self, event):
        index = self.selected_index()
        if index == wx.NOT_FOUND:
            self.error("Selecione uma conta na lista primeiro.", self.accounts)
            event.Skip()
            return
        account = self.manager.accounts[index]
        result = wx.MessageBox(
            f"Remover {account.name}, no valor de R$ {format_money(account.value)}?",
            "Confirmar remoção",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION,
            self,
        )
        if result == wx.YES:
            self.manager.remove_account(index)
            self.update_ui()
            self.set_status("Conta removida.")
            self.accounts.SetFocus()
        event.Skip()

    def on_toggle_paid(self, event):
        index = self.selected_index()
        if index == wx.NOT_FOUND:
            self.error("Selecione uma conta na lista primeiro.", self.accounts)
            event.Skip()
            return
        self.manager.toggle_paid(index)
        self.update_ui()
        self.accounts.SetSelection(index)
        self.accounts.SetFocus()
        item = self.manager.accounts[index]
        state = "paga" if item.paid else "pendente"
        self.set_status(f"Conta {item.name} marcada como {state}.")
        event.Skip()

    def on_calculate(self, event):
        self.update_ui()
        self.set_status(f"Cálculo atualizado. Saldo: R$ {format_money(self.manager.balance())}.")
        event.Skip()

    def on_new(self, event):
        if self.manager.salary == 0 and not self.manager.accounts:
            self.salary.SetFocus()
            event.Skip()
            return
        result = wx.MessageBox(
            "Uma nova análise apagará o salário e todas as contas atuais.",
            "Nova análise",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION,
            self,
        )
        if result == wx.YES:
            self.manager.reset()
            self.salary.Clear()
            self.account_name.Clear()
            self.account_value.Clear()
            self.category.SetValue("Outros")
            self.update_ui()
            self.salary.SetFocus()
            self.set_status("Nova análise iniciada.")
        event.Skip()

    def on_save(self, event):
        try:
            self.storage.save(self.manager)
            self.set_status("Análise salva com sucesso.")
            self.info("Análise salva com sucesso.")
        except Exception as error:
            self.error(f"Não foi possível salvar a análise. {error}")
        event.Skip()

    def on_load(self, event):
        try:
            self.storage.load(self.manager)
            self.salary.SetValue(format_money(self.manager.salary))
            self.update_ui()
            self.set_status("Análise carregada com sucesso.")
            self.info("Análise carregada com sucesso.")
        except FileNotFoundError as error:
            self.error(str(error))
        except Exception as error:
            self.error(f"Não foi possível carregar a análise. {error}")
        event.Skip()

    def on_export(self, event):
        try:
            self.storage.export_csv(self.manager)
            self.set_status("Contas exportadas para CSV.")
            self.info("Arquivo CSV exportado com sucesso.")
        except Exception as error:
            self.error(f"Não foi possível exportar o CSV. {error}")
        event.Skip()

    def on_focus_add(self, event):
        self.account_name.SetFocus()
        self.set_status("Foco no campo Nome da conta.")
        event.Skip()

    def on_help(self, event):
        dialog = HelpDialog(self)
        dialog.ShowModal()
        dialog.Destroy()
        event.Skip()

    def on_about(self, event):
        wx.MessageBox(
            f"{APP_NAME}\n\nVersão 1.0.\nPython + wxPython.\nInterface modular, com identidade visual inspirada na Dell.",
            "Sobre",
            wx.OK | wx.ICON_INFORMATION,
            self,
        )
        event.Skip()

    def on_exit(self, event):
        self.Close()

    def update_ui(self):
        previous = self.accounts.GetSelection()
        self.accounts.Freeze()
        try:
            self.accounts.Clear()
            for index, account in enumerate(self.manager.accounts, start=1):
                self.accounts.Append(
                    f"{index}. {account.name} | {account.category} | R$ {format_money(account.value)} | "
                    f"{'paga' if account.paid else 'pendente'}"
                )
        finally:
            self.accounts.Thaw()

        if self.manager.accounts:
            index = previous if 0 <= previous < len(self.manager.accounts) else 0
            self.accounts.SetSelection(index)
            account = self.manager.accounts[index]
            self.toggle.SetLabel("Marcar pendente" if account.paid else "Marcar paga")
        else:
            self.toggle.SetLabel("Marcar paga")

        self.result.update(self.manager.summary(), format_money)
        self.Layout()
        self.scroll.FitInside()

    def set_status(self, text):
        self.status.SetLabel(text)
        self.status_bar.SetStatusText(text)

    def info(self, text):
        wx.MessageBox(text, APP_NAME, wx.OK | wx.ICON_INFORMATION, self)

    def error(self, text, focus=None):
        wx.MessageBox(text, "Erro", wx.OK | wx.ICON_ERROR, self)
        if focus is not None:
            focus.SetFocus()

    def show_with_fade(self):
        self.Show()
        fade_in_window(self)
