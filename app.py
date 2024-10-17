### ROBÔ DE MONITORAMENTO DE PREÇO ####

# importações
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep 
import openpyxl
import datetime
import schedule


# criando a sheet
workbook = openpyxl.Workbook()

# Alterando o nome da sheet
workbook['Sheet'].title = 'Precos_Monitores'

# selecionando a sheet
sheet_precos_produtos = workbook['Precos_Monitores']

# Criando o cabeçalho da sheet
sheet_precos_produtos.append(['Produto','Data atual','Valor','Link'])


def rastreador_precos():

    def iniciar_driver():
        chrome_options = Options()
        # Fonte de opções de switches https://peter.sh/experiments/chromium-command-line-switches/

        arguments = ['--lang=pt-BR', '--start-maximized', '--incognito']

        for argument in arguments:
            chrome_options.add_argument(argument)

        driver = webdriver.Chrome(options=chrome_options)
        return driver

    driver = iniciar_driver()
    driver.get('https://www.zoom.com.br/search?q=monitor%2024%20polegadas')

    sleep(2)

    # Coletando nome do produto
    nome_produto = driver.find_element(By.XPATH,"//div/a[@class='ProductCard_ProductCard_Inner__gapsh']//div[2]//div[2]/div/div/h2").text

    # Coletando o valor do produto
    valor = driver.find_element(By.XPATH,"//div/a[@class='ProductCard_ProductCard_Inner__gapsh']//div[2]//div[2]/div[2]/p").text

    # tratando o valor do produto
    valor_tratado = valor.split()[1].replace(',','.')

    # Coletando o link do produto
    link = driver.find_element(By.XPATH,"//div/a[@class='ProductCard_ProductCard_Inner__gapsh']").get_attribute('href')

    # Coletando a data atual
    data_atual = datetime.date.today().strftime('%d/%m/%Y')

    #salvando os dados na planilha
    sheet_precos_produtos.append([nome_produto, data_atual, valor, link])

    # Salvando a sheet
    workbook.save(r'C:\projetos\Robo-de-monitoramento-diario-de-preco\arquivos\precos.xlsx')
    

# agendamento para de 30 em 30 minutos
schedule.every(30).minutes.do(rastreador_precos)

while True:
    schedule.run_pending()
    sleep(1)