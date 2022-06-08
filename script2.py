import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#FUNÇÃO PARA FORMATAR O NOME DO PRODUTO
def obterNome(nome):
  #SE FOR DO SITE COSMOS, REALIZAR A SEPARAÇÃO DO TITULO POR (-)
  if 'Cosmos' in nome:
    nome = nome.split(' - ')[0]
  # SE FOR DO SITE SHOPEE OU TELHANORTE, REALIZAR A SEPARAÇÃO DO TITULO POR (|)
  elif 'Shopee' in nome or 'Telhanorte' in nome:
    nome = nome.split(' | ')[0]
  # SE FOR DO SITE O COMPRA, REALIZAR A SEPARAÇÃO DO TITULO POR (à)
  elif 'OCompra' in nome:
    nome = nome.split(' à ')[0]
  return nome

#FUNÇÃO PARA CLASSIFICAR O PRODUTO A PARTIR DO NOME
def obterCat(nome):
  #SE CONTER PISCA OU LED OU TOM NO NOME, PARTE ELÉTRICA
  if 'PISCA' in nome or 'LED' in nome or 'TOM' in nome:
    categoria = 'ELÉTRICA'
  # SE CONTER TORNEIRA, PARTE HIDRÁULICA
  elif 'Torneira' in nome:
    categoria = 'HIDRÁULICA'
  else:
    categoria = nome.split(' ')[0]
  return categoria

#FUNÇÃO PARA OBTER O ENDEREÇO DA IMAGEM A PARTIR DO NOME E XPATH
def obterImg(driver,nome):
  if 'Cosmos' in nome:
    #captura a tag img do produto do site cosmo pelo xpath abaixo
    try:
      image = driver.find_element_by_xpath('//*[@id="product-gallery"]/div/img')
    except:
      image = 'DESCONHECIDA'
      return image
  elif 'Telhanorte' in nome:
    try:
      # captura a tag img do produto do site telhanorte pelo xpath abaixo
      image = driver.find_element_by_xpath('//*[@id="productImagesList"]/div/div/li/img[2]')
    except:
      image = 'DESCONHECIDA'
      return image
  elif 'OCompra' in nome:
    try:
      # captura a tag img do produto do site O Compra pelo xpath abaixo
      image = driver.find_element_by_xpath('//*[@id="imgGrande"]')
    except:
      image = 'DESCONHECIDA'
      return image
  else:
    image = 'DESCONHECIDA'
    return image
  src = image.get_attribute('src')
  return src

#opções de configuração do navegador, para não mostrar que é uma automatização
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#abre o navegador, com as opções carregadas
driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options)

#navega até o site de busca
try:
    driver.get('https://www.google.com/')
except:
    print('ERROR: Não foi possivel acessar o site de busca!')
    driver.close()
    exit()

#VARIAVEIS PARA ARMAZENAR TODOS OS DADOS
#arrays para armazenar o codigo, o nome do produto, a categoria e a imagem
nomesprodutos = []
listacod = []
listacat = []
listaimg = []

#LEITURA DA PLANILHA NO FORMATO CSV
with open('csv/ListadeProdutos2.csv', encoding='utf-8') as arquivo_referencia:
  #vai ler a tabela delimitado por virgulas
  tabela = csv.reader(arquivo_referencia, delimiter=',')
  #essa variavel é somente para pular a primeira linha
  linha = 0
  for l in tabela:
    #se for a primeira linha, não faz nada, só incrementa a linha
    if linha == 0:
        linha += 1
    #senao, realiza as operações seguintes
    else:
        #pega todos os dados da 5º coluna, que neste caso são os Codigo de barras
        cod = l[4]
        #verifica se a coluna não tem SEM GTIN e tem cod
        if not 'SEM GTIN' in cod and cod:
            #tratamento
            try:
                #captura o input de busca do google
                input_busca = driver.find_element_by_xpath('//input[@name="q"]')
            except:
                #se der erro ao capturar o input de busca do google, salva um nome qualquer para as variaveis
                print('ERROR: Não foi possivel realizar a busca')
                nome = 'ERROR'
                cat = 'ERROR'
                img = 'ERROR'
            else:
                #senão der erro na pagina, continua com as proximas operações
                #limpa o input
                input_busca.clear()
                #realiza a busca, passando o codigo de barras e dando ENTER
                input_busca.send_keys(cod + Keys.ENTER)
                #tempo de espera de 3seg
                time.sleep(3)
                #//*[@id="rso"]/div[1]//h3 (pegar o nome do produto pelo link do google)
                try:
                    #se o produto existir no sistema, vai acessar a primeira pagina
                    driver.find_element_by_xpath('//*[@id="rso"]/div[1]//h3').click()
                except:
                    #caso nao exista, salva um nome qualquer
                    nome = 'Produto Desconhecido'
                    cat = 'Categoria Desconhecida'
                    img = 'Imagem Desconhecida'
                else:
                    #espera de 5seg, para carregar a pagina acessada anteriormente
                    time.sleep(5)
                    #captura o titulo da pagina e realiza a formatação do nome
                    nome = obterNome(driver.title)
                    #captura a categoria a partir do nome
                    cat = obterCat(nome)
                    #captura a imagem a partir do title, xpath
                    img = obterImg(driver,driver.title)
                    #cat = nome.split(' ')[0]
                    #img = '{}.jpg'.format(nome)
                    driver.get('https://www.google.com/')
                    time.sleep(2)
            #por fim, armazena todos os dados obtidos
            listacod.append(cod)
            nomesprodutos.append(nome)
            listacat.append(cat)
            listaimg.append(img)
        else:
            #senao tem codigo de barras, armazena '-' em todos os dados desejados
            nomesprodutos.append('-')
            listacod.append('-')
            listacat.append('-')
            listaimg.append('-')
        #print('COD: {}'.format(listacod[linha-1]))
        #print('Produto: {}'.format(nomesprodutos[linha-1]))
        #print('Categoria: {}'.format(listacat[linha-1]))
        #print('Imagem: {}'.format(listaimg[linha-1]))
        #linha += 1

#GRAVANDO EM UMA NOVA PLANILHA
# 1. cria o arquivo
f = open('csv/Resultado.csv', 'w', newline='', encoding='utf-8')

# 2. cria o objeto de gravação
w = csv.writer(f)

#escreve a primeira linha
w.writerow(['EAN/GTIN','TITULO','CATEGORIA','IMAGE'])
for i in range(len(nomesprodutos)):
    #escreve as proximas linhas
    w.writerow([listacod[i],nomesprodutos[i],listacat[i],listaimg[i]])