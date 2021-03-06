import csv
import os
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


"""
#CONFIGURAÇÕES SELENIUM
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#LEITURA DE DADOS
while True:
    op = int(input('Informe 1 para URL única, 2 para uma lista de URL e 0 para finalizar\n').strip())
    if op == 1:
        saida = ''
        url = input('Informe a URL:\n').strip()
        xpath = input('Informe o Xpath:\n').strip()
        info = int(input('Informe o tipo da informação: 1 para textos/nomes e 2 para imagens\n').strip())
        driver = webdriver.Chrome(executable_path="driver/chromedriver.exe", options=options)
        try:
            driver.get(url)
        except:
            print('ERROR: Não foi possivel acessar a URL: {}'.format(url))
        else:
            time.sleep(3)
            if info == 1:
                try:
                    saida = driver.find_element_by_xpath(xpath).text
                except:
                    print('ERROR: Não foi possivel capturar o texto do xpath: {}'.format(xpath))
                else:
                    print('Saída: {}'.format(saida))
            elif info == 2:
                img = driver.find_element_by_xpath(xpath)
                nomeimg = 'image' #img.get_attribute('alt')
                src = img.get_attribute('src')
                if 'png' in src:
                    tipo = 'png'
                elif 'jpeg' in src:
                    tipo = 'jpeg'
                #os.makedirs('img')
                #urllib.request.urlretrieve(src, "img//{}.{}".format(nomeimg,tipo))
                urllib.request.urlretrieve(src, "{}.{}".format(nomeimg, tipo))
                #with open('my_picture.png', 'wb') as file:
                #    file.write(driver.find_element_by_xpath(xpath).screenshot_as_png)
                print('Imagem salva em: {}\\{}.{}'.format(os.getcwd(),nomeimg,tipo))
            else:
                print('ERROR: Opção inválida!')
        driver.close()
    elif op == 2:
        saida = []
        diretorio = input('Informe o caminho do arquivo CSV onde possui a lista de URL:\n').strip()
        col = int(input('Informe o numero da coluna, onde está a lista de URL:\n').strip())
        xpath = input('Informe o Xpath:\n').strip()
        info = int(input('Informe o tipo da informação: 1 para textos/nomes e 2 para imagens\n').strip())
        driver = webdriver.Chrome(executable_path="driver/chromedriver.exe", options=options)
        with open('{}'.format(diretorio), encoding='utf-8') as arquivo_referencia:
            # vai ler a tabela delimitando por virgulas
            tabela = csv.reader(arquivo_referencia, delimiter=',')
            # essa variavel é somente para pular a primeira linha
            linha = 0
            for l in tabela:
                # se for a primeira linha, não faz nada, só incrementa
                if linha == 0:
                    linha += 1
                # pula a primeira linha
                else:
                    urls = l[col-1]
                    if urls:
                        print(urls)
                        try:
                            driver.get(urls)
                        except:
                            print('ERROR: Não foi possivel acessar a URL da lista: {}'.format(urls))
                            break
                        else:
                            time.sleep(2)
                            if info == 1:
                                try:
                                    infotext = driver.find_element_by_xpath(xpath).text
                                except:
                                    print('ERROR: Não foi possivel capturar o texto do xpath: {}'.format(xpath))
                                    infotext = 'Produto Desconhecido'
                                saida.append(infotext)
                            elif info == 2:
                                try:
                                    img = driver.find_element_by_xpath(xpath)
                                except:
                                    print('ERROR: Não foi possivel capturar a imagem do xpath: {}'.format(xpath))
                                else:
                                    nomeimg = 'image {}'.format(linha)  # img.get_attribute('alt')
                                    src = img.get_attribute('src')
                                    if 'png' in src:
                                        tipo = 'png'
                                    elif 'jpeg' in src:
                                        tipo = 'jpeg'
                                    if not os.path.exists('img'):
                                        os.makedirs('img')
                                    urllib.request.urlretrieve(src, "img//{}.{}".format(nomeimg,tipo))
                                    saida.append('{}\\img\\{}.{}'.format(os.getcwd(),nomeimg,tipo))
                            else:
                                print('ERROR: Opção inválida!')
                    linha += 1
        if len(saida) > 0:
            print(saida)
        else:
            print('Não foi possivel realizar o webscraping')
        driver.close()
    elif op == 0:
        print('SCRIPT FINALIZADO!')
        break
    else:
        print('ERROR: Opção inválida! Por favor, tente novamente')
"""

"""
PRIMEIRA VERSÃO DO SCRIPT
#ABRINDO O NAVEGADOR PARA REALIZAR A BUSCA E CAPTURA DOS NOMES DOS PRODUTOS
#opções de configuração do navegador, para não mostrar que é uma automatização
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#abre o navegador, com as opções carregadas
driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options)
#navega até o site de busca
try:
    #driver.get('https://www.ean-search.org/')
    driver.get(url)
except:
    driver.close()

#LEITURA DA PLANILHA
#arrays para armazenar o cod e o nome do produto
nomesprodutos = []
listacod = []
#vai ler o arquivo csv
with open('csv/ListadeProdutos.csv', encoding='utf-8') as arquivo_referencia:
  #vai ler a tabela delimitando por virgulas
  tabela = csv.reader(arquivo_referencia, delimiter=',')
  #essa variavel é somente para pular a primeira linha
  linha = 0
  for l in tabela:
    #se for a primeira linha, não faz nada, só incrementa
    if linha == 0:
        linha += 1
    # pula a primeira linha
    else:
        #pega todos os dados da 5º coluna
        cod = l[4]
        #verifica se tem codigo e se não é SEM GTIN
        if not 'SEM GTIN' in cod and cod:
            #armazena o codigo na listacod
            listacod.append(cod)
            #tratamento
            try:
                # captura o input de busca codigo
                input_busca = driver.find_element_by_xpath('//input[@name="q"]')
            except:
                #se der erro na pagina, salva um nome qualquer
                nome = 'produto'
            else:
                #senão der erro na pagina, continua...
                #limpa o input
                input_busca.clear()
                #realiza a busca, passando o codigo e dando ENTER
                input_busca.send_keys(cod + Keys.ENTER)
                #captura o nome do produto, pelo xpath
                try:
                    #se o produto existir no sistema, pula o except
                    nome = driver.find_element_by_xpath('//*[@id="main"]/p[3]/b/a').text
                except:
                    #senao, se o produto não existir no sistema
                    try:
                        #captura o nome do mesmo jeito, pula o proximo except
                        nome = driver.find_element_by_xpath('//*[@id="main"]/p[1]/b').text
                    except:
                        #caso ocorra bloqueio devido pesquisa em massa, salva um nome qualquer
                        nome = 'produto'
            #por fim, armazena o nome na listadenomes
            nomesprodutos.append(nome)
        else:
            #senao tem codigo de barras, armazena '-' em ambas colunas
            nomesprodutos.append('-')
            listacod.append('-')

#GRAVANDO EM UMA NOVA PLANILHA
# 1. cria o arquivo
f = open('csv/NovaPlanilha.csv', 'w', newline='', encoding='utf-8')

# 2. cria o objeto de gravação
w = csv.writer(f)

#escreve a primeira linha
w.writerow(['EAN/GTIN','TITULO'])
for i in range(len(nomesprodutos)):
    #escreve as proximas linhas
    w.writerow([listacod[i],nomesprodutos[i]])
"""