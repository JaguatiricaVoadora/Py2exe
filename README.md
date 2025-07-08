# PyInstaller GUI Builder

Uma interface gráfica moderna para facilitar a criação de executáveis (.exe) a partir de scripts Python usando o PyInstaller.

## Como funciona
O PyInstaller GUI Builder permite que você:
- Selecione o arquivo principal do seu projeto Python.
- Configure opções comuns do PyInstaller (como `--onefile`, `--windowed`, `--noconfirm`, etc).
- Adicione arquivos de dados, ícone, imports ocultos e paths extras facilmente.
- Gere o comando PyInstaller automaticamente e execute a geração do executável sem precisar usar o terminal.
- Visualize logs do processo de build diretamente na interface.

A interface foi construída com Tkinter, usando o tema moderno `sv_ttk`.

## Como instalar

1. **Clone ou baixe o repositório**
2. Instale as dependências necessárias (de preferência em um ambiente virtual):

```bash
pip install -r requirements.txt
```

## Como usar

1. Execute o aplicativo:

```bash
python Py2EXE.py
```

2. Na janela que abrir:
   - Clique em "Selecionar" e escolha o arquivo Python principal do seu projeto.
   - Marque/desmarque as opções desejadas (ex: `--onefile` para gerar um único .exe, `--windowed` para não abrir console, etc).
   - (Opcional) Adicione arquivos de dados, ícone, imports ocultos ou paths extras conforme necessidade.
   - Clique em "Gerar EXE" para iniciar o processo.
   - O progresso e logs serão exibidos na interface.
   - Ao final, o executável será gerado na pasta `dist`.

## Requisitos
- Python 3.7+
- Windows

## Dependências principais
- `tkinter`
- `sv-ttk`
- `pyinstaller`

Todas as dependências podem ser instaladas via o `requirements.txt`.

## Observações
- O PyInstaller precisa estar disponível no PATH do sistema (ao instalar pelo `pip`, normalmente já fica).
- O app foi feito para facilitar a vida de quem não quer lidar com comandos no terminal para gerar executáveis de scripts Python.

---

Sinta-se à vontade para sugerir melhorias ou reportar problemas!
