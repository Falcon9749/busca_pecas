import os
import time
import json
import re
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import and_
import click

# Imports do Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# --- Configurações Iniciais ---
load_dotenv()
app = Flask(__name__)

# --- Configuração do Banco de Dados ---
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Variáveis de ambiente do banco de dados (DB_USER, etc.) não foram definidas no arquivo .env!")

database_uri = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Inicialização do Banco de Dados e Migração ---
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- Modelo do Banco de Dados ---
class Part(db.Model):
    __tablename__ = 'parts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    seller = db.Column(db.String(100))
    link = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.String(100), unique=True, nullable=False)
    car_model = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    scraped_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'price': self.price, 
            'seller': self.seller, 
            'link': self.link, 
            'car_model': self.car_model,
            'image_url': self.image_url
        }

# --- COMANDOS CUSTOMIZADOS DE TERMINAL ---

@app.cli.command("db-drop")
@click.confirmation_option(prompt="Você tem certeza que quer apagar todo o banco de dados?")
def db_drop():
    """Apaga todas as tabelas do banco de dados."""
    db.drop_all()
    print("Banco de dados apagado com sucesso.")

@app.cli.command("scrape")
def scrape_data():
    """
    Scraper otimizado que reinicia o navegador a cada nova busca para economizar memória.
    Usa a lista de peças completa.    
    
    Scraper otimizado que lê a lista de peças de um arquivo JSON externo.
    """
    try:
        with open('search_list.json', 'r', encoding='utf-8') as f:
            parts_to_search = json.load(f)
        print(f"{len(parts_to_search)} tipos de peças carregados do arquivo 'search_list.json'.")
    except FileNotFoundError:
        print("ERRO: Arquivo 'search_list.json' não encontrado. Usando uma lista de emergência.")
        parts_to_search = ["amortecedor", "farol"] # Lista de fallback caso o arquivo não exista
    
    cars_to_scrape = [
        {"model_name": "Hyundai HB20 2021", "search_model": "hb20 2021"},
        {"model_name": "Fiat Uno Vivace 2014", "search_model": "uno vivace 2014"},
    ]
    
    total_pages_to_scrape = 10 # Comece com 2 ou 3 páginas por peça para não demorar demais

    print("--- INICIANDO SCRAPING OTIMIZADO ---")

    for car in cars_to_scrape:
        print(f"\n--- Procurando peças para: '{car['model_name']}' ---")
        for part_name in parts_to_search:
            search_term = f"{part_name} {car['search_model']}"
            print(f"  > Buscando por: '{search_term}'...")

            driver = None
            try:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                
                driver.get("https://www.mercadolivre.com.br")
                with open('cookies.json', 'r') as f: cookies = json.load(f)
                for cookie in cookies:
                    if 'sameSite' in cookie and cookie['sameSite'] not in ['Strict', 'Lax', 'None']:
                        cookie['sameSite'] = 'Lax'
                    driver.add_cookie(cookie)

                for page_number in range(1, total_pages_to_scrape + 1):
                    search_term_formatted = search_term.replace(' ', '-')
                    if page_number == 1:
                        url = f"https://lista.mercadolivre.com.br/{search_term_formatted}"
                    else:
                        offset = 48 * (page_number - 1) + 1
                        url = f"https://lista.mercadolivre.com.br/{search_term_formatted}_Desde_{offset}"
                    
                    driver.get(url)
                    time.sleep(2)
                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    items = soup.find_all('div', class_='ui-search-result__wrapper')

                    if not items:
                        print(f"    Página {page_number}: Nenhum item encontrado.")
                        break

                    new_parts_count_page = 0
                    for item in items:
                        name_element = item.find('a', class_='poly-component__title')
                        price_element = item.find('span', class_='andes-money-amount__fraction')
                        symbol_element = item.find('span', class_='andes-money-amount__currency-symbol')
                        link_element = name_element
                        image_element = item.find('img', class_='poly-component__picture')
                        image_url = image_element.get('data-src') or image_element.get('src') if image_element else None
                        
                        if name_element and link_element:
                            link = link_element['href']
                            match = re.search(r'(MLB-\d+)', link)
                            if not match: continue
                            product_id = match.group(1)
                            if Part.query.filter_by(product_id=product_id).first(): continue
                            
                            price_str = f"{symbol_element.text.strip() if symbol_element else ''} {price_element.text.strip() if price_element else 'A consultar'}"
                            
                            new_part = Part(name=name_element.text.strip(), price=price_str, seller="Mercado Livre", link=link, product_id=product_id, car_model=car['model_name'], image_url=image_url)
                            db.session.add(new_part)
                            new_parts_count_page += 1
                    
                    db.session.commit()
                    print(f"    Página {page_number}: {new_parts_count_page} novas peças adicionadas.")
            
            except Exception as e:
                print(f"    Ocorreu um erro ao buscar '{search_term}': {e}")
                db.session.rollback()
            
            finally:
                if driver:
                    driver.quit()
                    print(f"  > Busca por '{search_term}' concluída. Navegador fechado.")
    
    print("\n--- SCRAPING GERAL CONCLUÍDO! ---")

# --- ROTAS DA APLICAÇÃO WEB ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search')
def search_parts():
    query = request.args.get('q')
    model = request.args.get('model')
    if not query: return jsonify([])
    filters = [Part.name.ilike(f"%{query}%")]
    if model:
        for word in model.split():
            filters.append(Part.name.ilike(f"%{word}%"))
    parts_from_db = Part.query.filter(and_(*filters)).limit(30).all()
    results = [part.to_dict() for part in parts_from_db]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)