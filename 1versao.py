import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#PRIMEIRA VERSÃO DO SCRIPT
#ABRINDO O NAVEGADOR PARA REALIZAR A BUSCA E CAPTURA DOS NOMES DOS PRODUTOS
#opções de configuração do navegador, para não mostrar que é uma automatização
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#abre o navegador, com as opções carregadas
driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options)
#navega até o site de busca
try:
    driver.get('https://www.ean-search.org/')
    #driver.get(url)
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