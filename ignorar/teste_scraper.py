import requests
from bs4 import BeautifulSoup

# --- CONFIGURE SEU TESTE AQUI ---
TARGET_URL = "https://lista.mercadolivre.com.br/pecas-hb20"

# --- DEIXE SUAS PISTAS AQUI ---
#    Sua missão é preencher com as TAGs e CLASSes corretas que você encontrar
CONTAINER_TAG = 'div'
CONTAINER_CLASS = 'ui-search-result__wrapper' # <-- Provavelmente incorreto

TITLE_TAG = 'h2'
TITLE_CLASS = 'ui-search-item__title'

PRICE_TAG = 'span'
PRICE_CLASS = 'andes-money-amount__fraction'

LINK_TAG = 'a'
LINK_CLASS = 'ui-search-link'

IMAGE_TAG = 'img'
IMAGE_CLASS = 'ui-search-result-image__element'


# --- LÓGICA DO TESTE (Não precisa mexer abaixo) ---
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
print(f"Acessando: {TARGET_URL}")
try:
    response = requests.get(TARGET_URL, headers=headers)
    response.raise_for_status()
    with open("debug_pagina_atual.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("!!! Arquivo 'debug_pagina_atual.html' salvo para sua análise. !!!")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all(CONTAINER_TAG, class_=CONTAINER_CLASS)
    
    print("-" * 30)
    print(f"Contêineres de produto encontrados: {len(items)}")
    print("-" * 30)

    if items:
        print("\nAnalisando o primeiro item encontrado:")
        item = items[0]
        title = item.find(TITLE_TAG, class_=TITLE_CLASS)
        price = item.find(PRICE_TAG, class_=PRICE_CLASS)
        link = item.find(LINK_TAG, class_=LINK_CLASS)
        image = item.find(IMAGE_TAG, class_=IMAGE_CLASS)
        
        print(f"Título: {title.text.strip() if title else 'NÃO ENCONTRADO'}")
        print(f"Preço: {price.text.strip() if price else 'NÃO ENCONTRADO'}")
        print(f"Link: {link['href'] if link else 'NÃO ENCONTRADO'}")
        print(f"Imagem: {image.get('data-src') or image.get('src') if image else 'NÃO ENCONTRADA'}")
except Exception as e:
    print(f"\nOcorreu um erro: {e}")





                    name_element = item.find('a', class_='poly-component__title')
                    price_element = item.find('span', class_='andes-money-amount__fraction')
                    symbol_element = item.find('span', class_='andes-money-amount__currency-symbol')
                    link_element = name_element
                    image_element = item.find('img', class_='poly-component__picture')
                    image_url = image_element.get('data-src') or image_element.get('src') if image_element else None