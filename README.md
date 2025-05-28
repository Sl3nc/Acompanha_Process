# Consulta Processual Automatizada

Este projeto é uma aplicação desktop para automatizar a consulta de processos judiciais em diferentes tribunais brasileiros, utilizando automação web (Selenium) e interface gráfica (Qt/PySide6).

## Funcionalidades

- **Leitura de arquivo Excel**: O usuário seleciona um arquivo `.xlsx` contendo uma lista de números de processos.
- **Consulta automática**: O programa acessa os sites dos tribunais (EPROC e PJE), realiza a consulta dos processos e extrai os movimentos processuais.
- **Tratamento de captcha**: Quando necessário, o programa exibe a imagem do captcha para o usuário digitar a resposta.
- **Atualização do arquivo**: Os resultados das consultas são inseridos no arquivo Excel original.
- **Interface gráfica amigável**: Barra de progresso, mensagens de aviso e feedback visual durante o processamento.
- **Suporte a múltiplos tribunais**: Estrutura preparada para adicionar novos tribunais facilmente.

## Como funciona

1. **Seleção do arquivo**: O usuário clica no botão para anexar o relatório de processos em formato Excel.
2. **Processamento**: Ao iniciar, o programa lê os números de processos e inicia a consulta automática em cada tribunal correspondente.
3. **Captcha**: Se o site exigir captcha, a imagem é exibida e o usuário deve informar o texto.
4. **Resultados**: Os movimentos processuais são inseridos no arquivo Excel e o arquivo é aberto automaticamente ao final.

## Estrutura do Projeto

- `code/index.py`: Código principal da aplicação, contendo as classes de manipulação de arquivos, automação web, lógica de consulta e interface gráfica.
- `src/window_process.py`: Arquivo gerado pelo Qt Designer com a definição da interface gráfica.
- `src/imgs/`: Imagens utilizadas na interface (ícones, logo, GIF de carregamento).
- `src/drivers/chromedriver.exe`: Driver do Chrome para automação via Selenium.

## Principais Classes

- **Arquivo**: Manipula o arquivo Excel de entrada e saída.
- **Browser**: Cria e configura o navegador Chrome para automação.
- **Tribunal (abstrata)**: Interface para implementação de consultas em diferentes tribunais.
- **EPROC/PJE**: Implementações específicas para cada tribunal.
- **Juiz**: Orquestra a consulta dos processos, gerenciando threads e sinais para a interface.
- **MainWindow**: Interface gráfica principal, gerencia interações do usuário e fluxo do programa.

## Requisitos

- Python 3.8+
- Bibliotecas: `selenium`, `PySide6`, `pandas`, `openpyxl`, `Pillow`, `unidecode`
- Chrome instalado e compatível com o `chromedriver.exe` fornecido

## Instalação

1. Clone este repositório.
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute o programa:
   ```
   python code/index.py
   ```

## Observações

- O programa foi desenvolvido para uso em ambiente Windows.
- O arquivo Excel deve conter os números dos processos na coluna E.
- Novos tribunais podem ser adicionados implementando subclasses de `Tribunal`.

## Licença

Este projeto é de uso interno e não possui licença aberta.
