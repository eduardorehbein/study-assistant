# Assistente de Estudos

Este projeto é um Assistente de Estudos interativo que gera um calendário de estudos personalizado com base no tema e no tempo disponível informado pelo usuário. O calendário é salvo automaticamente em um arquivo CSV na pasta `results`, facilitando sua importação em ferramentas de visualização de tabelas como o Google Sheets ou o Excel.

## Propósito
O Assistente de Estudos foi criado para ajudar estudantes e autodidatas a organizarem seus estudos de forma eficiente, utilizando inteligência artificial para planejar sessões de estudo personalizadas.

## Como executar o projeto

### 1. Pré-requisitos
- Python 3.8 ou superior
- [pip](https://pip.pypa.io/en/stable/)
- Uma chave de API do Google (defina a variável de ambiente `GOOGLE_API_KEY` no arquivo `.env` na raiz do projeto)

### 2. Instalação e execução nativa

1. **Clone o repositório:**
   ```bash
   git clone git@github.com:eduardorehbein/study-assistant.git
   cd study-assistant
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente:**
   - Altere o arquivo `.env` na raiz do projeto para que utilize sua chave de API:
     ```env
     GOOGLE_API_KEY="SuaChaveAqui"
     ```

4. **Execute o programa:**
   ```bash
   python main.py
   ```

5. **Siga as instruções na tela** para informar o tema e o tempo disponível. O calendário será salvo em `results/<tema>.csv`.

## Executando no DevContainer do VS Code

1. **Abra o projeto no VS Code.**
2. Certifique-se de que a extensão "Dev Containers" está instalada.
3. Clique em "Reabrir no Container" quando solicitado, ou pressione `F1` e selecione `Dev Containers: Reopen in Container`.
4. Aguarde a configuração do ambiente.
5. **Configure as variáveis de ambiente:**
   - Altere o arquivo `.env` na raiz do projeto para que utilize sua chave de API:
     ```env
     GOOGLE_API_KEY="SuaChaveAqui"
6. **No terminal do VS Code, execute:**
   ```bash
   python main.py
   ```
7. Siga as instruções na tela.

## Resultados
O calendário de estudos gerado será salvo automaticamente na pasta `results` com o nome do tema escolhido. Como resultado intermediário do processo, pode-se visualizar no terminal o plano de ensino gerado pelo primeiro agente do sistema, que serve como base para a montagem do calendário.
