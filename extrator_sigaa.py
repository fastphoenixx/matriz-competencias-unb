import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import os

# --- CONFIGURAÇÕES ---
ARQUIVO_HTML = 'SIGAA.html' 
NOME_ARQUIVO_SAIDA = 'disciplinas_obrigatorias_unb.csv'
URL_SIGAA_LISTA = "https://sigaa.unb.br/sigaa/graduacao/curriculo/lista.jsf"

# Caminhos Arch Linux
CAMINHO_CHROMIUM = "/usr/bin/chromium"
CAMINHO_DRIVER = "/usr/bin/chromedriver"

def extrair_ids_do_html_local():
    print(f"Lendo arquivo local: {ARQUIVO_HTML}...")
    if not os.path.exists(ARQUIVO_HTML):
        print(f"[ERRO] O arquivo '{ARQUIVO_HTML}' não existe na pasta atual.")
        return pd.DataFrame()

    try:
        with open(ARQUIVO_HTML, 'r', encoding='iso-8859-1') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"[ERRO] Falha ao abrir HTML: {e}")
        return pd.DataFrame()

    disciplinas = []
    paineis = soup.find_all('td', {'class': 'rich-tabpanel-content'})
    
    for painel in paineis:
        titulo = painel.find('span', style=re.compile('font-weight: bold'))
        if not titulo or 'Nível' not in titulo.text:
            continue
        semestre = titulo.text.strip().replace('Nível', '').strip()
        
        linhas = painel.find_all('tr', class_=re.compile('linha(Par|Impar)'))
        for linha in linhas:
            colunas = linha.find_all('td')
            if len(colunas) < 2: continue
            tag_label = colunas[0].find('label')
            if not tag_label: continue
                
            codigo = tag_label.text.strip()
            match_id = re.search(r'show\((\d+),', tag_label.get('onclick', ''))
            id_interno = match_id.group(1) if match_id else None
            
            texto = colunas[1].text.strip()
            nome, ch = (texto.rsplit(' - ', 1)) if ' - ' in texto else (texto, "N/A")
            
            disciplinas.append({
                'semestre': semestre, 'id_interno': id_interno, 'codigo': codigo,
                'nome': nome, 'ch_detalhada': ch, 'natureza': 'Obrigatória'
            })
    return pd.DataFrame(disciplinas)

def limpar_texto_inteligente(soup_pagina):
    """
    Estratégia TEXTO PURO: Converte tudo para string e corta o recheio.
    """
    # 1. Converte o HTML inteiro para texto, usando um separador único
    texto_completo = soup_pagina.get_text(" | ", strip=True)
    
    # Palavras-chave que delimitam a ementa
    # O SIGAA varia entre "Ementa/Descrição", "Ementa" ou "Descrição"
    marcadores_inicio = ["Ementa/Descrição", "Ementa / Descrição", "Ementa:", "Descrição:"]
    marcadores_fim = ["Bibliografia", "Outras informações", "Matriculável", "Fechar", "Programa"]

    texto_inicio = None
    marcador_usado = ""

    # 2. Encontra onde começa a ementa
    for marcador in marcadores_inicio:
        if marcador in texto_completo:
            texto_inicio = texto_completo.split(marcador, 1)[1]
            marcador_usado = marcador
            break
    
    if texto_inicio is None:
        return "Ementa não encontrada no texto da página"

    # 3. Encontra onde termina (no primeiro marcador de fim que aparecer)
    menor_indice = len(texto_inicio)
    texto_cortado = texto_inicio

    for fim in marcadores_fim:
        indice = texto_inicio.find(fim)
        if indice != -1 and indice < menor_indice:
            menor_indice = indice
            texto_cortado = texto_inicio[:indice]

    # 4. Limpeza final de formatação
    ementa_limpa = texto_cortado.strip(" |:-")
    
    # Remove resquícios comuns do pipe
    if ementa_limpa.startswith("|"): ementa_limpa = ementa_limpa[1:].strip()
    
    return ementa_limpa

def buscar_ementas_selenium(df):
    print("\n--- INICIANDO O NAVEGADOR (MODO TEXTO PURO) ---")
    options = Options()
    options.binary_location = CAMINHO_CHROMIUM
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    
    service = Service(CAMINHO_DRIVER)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL_SIGAA_LISTA)

    print("\n" + "="*60)
    print("AÇÃO NECESSÁRIA: Faça o login e navegue até a lista de matérias.")
    print("Certifique-se que a lista está visível.")
    print("VOLTE AQUI e aperte ENTER.")
    print("="*60 + "\n")
    input("Aguardando ENTER...")

    ementas = []
    total = len(df)

    # Remove barra de loading para não atrapalhar prints
    try: driver.execute_script("if(document.getElementById('painel-mensagem-envio')) document.getElementById('painel-mensagem-envio').style.display='none';")
    except: pass

    for index, row in df.iterrows():
        cod = row['codigo']
        print(f"[{index+1}/{total}] {cod}...", end=" ")

        try:
            # Abre o modal
            driver.execute_script(f"PainelComponente.show({row['id_interno']},'/sigaa/graduacao/componente_programa/view_panel_programa_relatorio.jsf');")
            
            # Espera fixa para garantir carga
            time.sleep(2) 

            # Captura o HTML e processa como texto puro
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')
            
            ementa = limpar_texto_inteligente(soup)
            
            # Validação básica
            if len(ementa) > 5 and "não encontrada" not in ementa:
                print("OK")
            else:
                print(f"Vazio/Erro: {ementa[:30]}...")

            ementas.append(ementa)

            # Fecha com ESC
            ActionChains(driver).send_keys('\ue00c').perform() 
            time.sleep(0.5)

        except Exception as e:
            print(f"Erro: {e}")
            ementas.append("ERRO_CRITICO")
            try: ActionChains(driver).send_keys('\ue00c').perform() 
            except: pass

    driver.quit()
    return ementas

if __name__ == "__main__":
    df = extrair_ids_do_html_local()
    if not df.empty:
        print(f"Encontradas {len(df)} disciplinas.")
        lista = buscar_ementas_selenium(df)
        
        if len(lista) < len(df):
             df = df.iloc[:len(lista)]
             
        df['Ementa/Descrição'] = lista
        
        cols = ['Código da Disciplina', 'Nome da Disciplina', 'CH Detalhada', 'Natureza', 'Ementa/Descrição']
        df.rename(columns={'codigo': 'Código da Disciplina', 'nome': 'Nome da Disciplina', 'ch_detalhada': 'CH Detalhada', 'natureza': 'Natureza'}, inplace=True)
        
        df[cols].to_csv(NOME_ARQUIVO_SAIDA, index=False, sep=';', encoding='utf-8-sig')
        print(f"\n[SUCESSO] Arquivo salvo: {NOME_ARQUIVO_SAIDA}")
