from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TextArea, Static, Input
from textual.screen import Screen
from textual.binding import Binding


class TelaPadrao(Screen):

    BINDINGS = [
        Binding('ctrl+t', 'abrir_arquivo', 'Abrir arquivo'),
        Binding('ctrl+s', 'salvar_arquivo', 'Salvar novo arquivo'),
        Binding('ctrl+l', 'limpar_arquivo', 'Limpar'),
    ]

    def compose(self) -> ComposeResult:

        yield Header(show_clock=True, time_format="%X")

        yield TextArea(show_line_numbers=True, id='text_area')
        yield Input(placeholder='Adicione o nome do arquivo (nome.extensao)', id='in_nome_arquivo')

        yield Footer(show_command_palette=False)

    def validar_nome_arquivo(self):
        nome_arquivo = str(self.query_one('#in_nome_arquivo', Input).value)

        if nome_arquivo == "":
            self.notify('Insira um nome para o arquivo!')
        elif '.' not in nome_arquivo:
            self.notify('Adicione uma extensão ao arquivo!')
        else:
            return nome_arquivo

    def action_abrir_arquivo(self):
        nome_arquivo = self.validar_nome_arquivo()

        try:
            with open(f'{nome_arquivo}', 'r+', encoding='utf-8') as arquivo:
                conteudo_arquivo = str(arquivo.read())
                self.query_one('#text_area', TextArea).text = conteudo_arquivo

        except FileNotFoundError:
            self.notify('Arquivo não encontrado!')

    def action_salvar_arquivo(self):
        nome_arquivo = self.validar_nome_arquivo()
        texto_escrito = self.query_one("#text_area", TextArea).text

        if nome_arquivo:
            with open(f'{nome_arquivo}', 'w', encoding='utf-8') as arquivo:
                arquivo.write(texto_escrito)

    def action_limpar_arquivo(self):
        self.query_one('#text_area', TextArea).text = ''


class NanoApp(App):
    CSS_PATH = "nano_textual.css"

    SCREENS = {
        'tela_padrao': TelaPadrao,
    }

    TITLE = "Nano"
    SUB_TITLE = "Tela inicial"

    def compose(self) -> ComposeResult:
        yield Static()

    def on_mount(self):
        self.push_screen('tela_padrao')


if __name__ == "__main__":
    app = NanoApp()
    app.run()
