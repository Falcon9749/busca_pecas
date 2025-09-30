# Busca Peças PRO

Um agregador inteligente de preços de peças automotivas, construído com Python, Flask e Selenium.

## 📝 Visão Geral

O mercado de peças automotivas é vasto e descentralizado, dificultando a comparação de preços para consumidores e oficinas. O Busca Peças PRO resolve este problema ao automatizar a coleta de dados de múltiplos varejistas online, consolidando as informações em um banco de dados local e apresentando-as em uma interface web rápida e fácil de usar.

## ✨ Features Principais

* **Scraping Multi-Fonte:** Estrutura modular para coletar dados do Mercado Livre e facilmente extensível para outras fontes.
* **Busca Inteligente:** Permite ao usuário filtrar peças por nome e por modelo/ano do veículo, refinando os resultados.
* **Banco de Dados Persistente:** Utiliza PostgreSQL para armazenar os dados coletados, garantindo buscas quase instantâneas.
* **Anti-Bot Bypass:** Emprega Selenium e gerenciamento de cookies para simular a navegação humana, superando proteções anti-scraping e telas de login.
* **Prevenção de Duplicatas:** Usa o ID único do produto (código MLB) para garantir que cada peça seja salva no banco de dados apenas uma vez.
* **Interface Limpa:** Frontend desenvolvido com HTML/CSS/JavaScript e Bootstrap, com estrutura de arquivos organizada.
* **Configuração Segura:** Utiliza variáveis de ambiente (`.env`) para gerenciar senhas e configurações de banco de dados.
* **Gerenciamento de Banco de Dados:** Usa Flask-Migrate para controlar as versões do schema do banco de dados de forma profissional.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript, Bootstrap
* **Banco de Dados:** PostgreSQL, SQLAlchemy, Flask-Migrate
* **Web Scraping:** Selenium, BeautifulSoup, WebDriver-Manager
* **Ferramentas:** Git, Venv, python-dotenv

## ⚙️ Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e rodar a aplicação na sua máquina.

### Pré-requisitos
* Python 3.10+
* PostgreSQL
* Google Chrome instalado

### Passos
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Falcon9749/busca_pecas.git]
    cd [busca_pecas]
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    # Criar o venv
    python -m venv venv
    # Ativar (Windows Git Bash)
    source venv/Scripts/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados:**
    * Crie um banco de dados no PostgreSQL chamado `pecas_db`.
    * Crie um arquivo `.env` na raiz do projeto com base no exemplo abaixo, preenchendo com suas credenciais:
        ```
        DB_USER="postgres"
        DB_PASSWORD="sua_senha"
        DB_HOST="localhost"
        DB_PORT="5432"
        DB_NAME="pecas_db"
        ```

5.  **Configure os Cookies:**
    * Instale a extensão [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) no Chrome.
    * Acesse e faça login no `mercadolivre.com.br`.
    * Clique no ícone da extensão e em "Exportar".
    * Crie um arquivo `cookies.json` na raiz do projeto e cole o conteúdo exportado nele.

6.  **Crie as tabelas do banco:**
    ```bash
    python -m flask db upgrade
    ```

7.  **Popule o banco de dados (este processo é demorado!):**
    ```bash
    python -m flask scrape
    ```

8.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

9.  **Acesse no navegador:**
    Abra [http://localhost:5000](http://localhost:5000) no seu navegador.

## 🚀 Próximos Passos
* [ ] Adicionar mais fontes de scraping (Amazon, Magazine Luiza, lojas especializadas).
* [ ] Adicionar ordenação de resultados (por preço, relevância).
* [ ] Implementar paginação no frontend para buscas com muitos resultados.
* [ ] Automatizar a execução do scraper com um agendador de tarefas (Cron/Agendador do Windows).
* [ ] Fazer o deploy da aplicação para um servidor na nuvem (Heroku/Render).

## 👨‍💻 Autor
**[Gilnei Monteiro]**
* LinkedIn: [[@gilnei-monteiro](https://www.linkedin.com/in/gilnei-monteiro/)]
* GitHub: [[Falcon9749](https://github.com/Falcon9749/busca_pecas.git)]