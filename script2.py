import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#LEITURA DO CÓDIGO DE BARRAS DO ARQUIVO CSV
print('REALIZANDO A LEITURA DA PLANILHA...')
listacod = []
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
        if cod:
            listacod.append(cod)
        else:
            listacod.append('-')
print('LEITURA DA PLANILHA CONCLUÍDA')


#VARIAVEIS PARA ARMAZENAR OS PRODUTOS, MARCAS, CATEGORIAS, SUBCATEGORIA, IMAGEM
nomesprodutos = []
listamarca = []
listacat = []
listasubcat = []
listaimg = []

#OPÇÕES DE CONFIGURAÇÃO DO NAVEGADOR
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#ABRIR O NAVEGADOR, COM AS CONFIGURAÇÕES AJUSTADAS ANTERIORMENTE
print('ABRINDO O NAVEGADOR')
driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options)

"""
urlsbusca = ['https://www.americanas.com.br/','https://www.amazon.com.br/','https://www.palacio.com.br/',
             'https://www.ramada.com.br/','https://www.lojadomecanico.com.br/','https://www.amazon.com.br/',
             'https://www.telhanorte.com.br/','https://www.google.com/']
"""

#URLS DE BUSCAS DE PRODUTOS
urlsbusca = ['https://www.amazon.com.br/','https://www.google.com.br/']

#ll = 0
#ACESSANDO OS SITES DE BUSCAS, REALIZANDO A BUSCA E TRAZENDO AS INFORMAÇÕES NECESSÁRIAS
print('GERANDO O RESULTADO...')
for cod in listacod:
    #caso exista codigo de barras e não seja SEM GTIN, realizar a operação de buscar informações
    if cod and not 'SEM GTIN' in cod:
        for url in urlsbusca:
            #vai acessar todas as urls de buscas presente na lista urlsbusca
            try:
                driver.get(url)
            except:
                #senao conseguiu acessar, vai exibir e pular para o proximo site
                print('ERROR: Não foi possivel acessar a URL: {}'.format(url))
                continue
            else:
                # Tempo para carregar o presente site
                time.sleep(5)
                # Verificar o site corrente e realizar o tratamento de acordo cada site
                if 'amazon.com.br' in url:
                    # buscar o produto pelo codigo
                    try:
                        input_busca = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
                    except:
                        continue
                    else:
                        input_busca.clear()
                        input_busca.send_keys(cod + Keys.ENTER)
                        time.sleep(3)

                    #verificar se encontrou o resultado, se sim, vai ter a imagem
                    try:
                        driver.find_element_by_xpath('//img[@class="s-image"]').click()
                    except:
                        #senao ter imagem, não encontrou o resultado, buscar no proximo site
                        continue
                    else:
                        #se ter resultado, capturar os atributos do produto
                        nameproduto = driver.find_element_by_xpath('//*[@id="productTitle"]').text
                        marca = driver.find_element_by_xpath('//*[@id="bylineInfo"]').text
                        marca = marca.split(':')[1].strip()
                        img = driver.find_element_by_xpath('//*[@id="landingImage"]').get_attribute('src')
                        categorias = driver.find_elements_by_xpath('//*[@id="nav-subnav"]/a')
                        cat = categorias[0].text
                        subcat = categorias[len(categorias)-1].text
                        if subcat == '':
                            subcat = 'null'
                        #adicionar os atributos nas listas
                        nomesprodutos.append(nameproduto)
                        listamarca.append(marca)
                        listacat.append(cat)
                        listasubcat.append(subcat)
                        listaimg.append(img)

                        #parar o loop de urls de buscas
                        break
                elif 'google.com.br' in url:
                    #buscar pelo produto
                    try:
                        input_busca = driver.find_element_by_xpath('//input[@name="q"]')
                    except:
                        nomesprodutos.append('desconhecido')
                        listamarca.append('desconhecida')
                        listacat.append('desconhecida')
                        listasubcat.append('desconhecida')
                        listaimg.append('desconhecida')
                        break
                    else:
                        input_busca.clear()
                        #utilizei a magazineluiza pois trás resultados mais completos das informações desejadas
                        input_busca.send_keys(cod + Keys.ENTER)
                        time.sleep(3)
                    #verificar o resultado da pesquisa
                    try:
                        #acessar o primeiro site encontrado pelo google
                        elementos = driver.find_elements_by_xpath('//*[@id="rso"]//div//a')
                    except:
                        #caso não encontre nenhum resultado, atribui desconhecido para todos
                        nomesprodutos.append('desconhecido')
                        listamarca.append('desconhecida')
                        listacat.append('desconhecida')
                        listasubcat.append('desconhecida')
                        listaimg.append('desconhecida')
                        break
                    else:
                        time.sleep(3)
                        linkmagalu = ''
                        for link in elementos:
                            if 'www.magazineluiza.com.br' in link.get_attribute('href'):
                                linkmagalu = link.get_attribute('href')
                                break
                        if linkmagalu != '':
                            try:
                                driver.get(linkmagalu)
                            except:
                                nomesprodutos.append('desconhecido')
                                listamarca.append('desconhecida')
                                listacat.append('desconhecida')
                                listasubcat.append('desconhecida')
                                listaimg.append('desconhecida')
                                break
                            time.sleep(5)
                            try:
                                driver.find_element_by_xpath('//button[@data-testid="button-message-box"]').click()
                            except:
                                pass
                            else:
                                time.sleep(1)
                                driver.find_element_by_xpath('//div[@class="container-button-banner"]').click()
                            time.sleep(5)

                            # capturar as informações desejadas do site
                            try:
                                nameproduto = driver.find_element_by_xpath('//*[@data-testid="heading-product-title"]').text
                            except:
                                #caso bloqueia a busca na magazine luiza
                                nomesprodutos.append('desconhecido')
                                listamarca.append('desconhecida')
                                listacat.append('desconhecida')
                                listasubcat.append('desconhecida')
                                listaimg.append('desconhecida')
                                break
                            else:
                                nameproduto = nameproduto.split(' - ')[0]
                            marca = driver.find_element_by_xpath('//*[@data-testid="heading-product-brand"]').text
                            img = driver.find_element_by_xpath('//img[@data-testid="image-selected-thumbnail"]').get_attribute('src')
                            categorias = driver.find_elements_by_xpath('//*[@data-testid="breadcrumb-item-list"]')
                            cat = categorias[2].text
                            subcat = categorias[3].text

                            # adicionar as informações obtidas nas listas
                            nomesprodutos.append(nameproduto)
                            listamarca.append(marca)
                            listacat.append(cat)
                            listasubcat.append(subcat)
                            listaimg.append(img)

                            # parar o loop de urls de busca
                            break
                        else:
                            nomesprodutos.append('desconhecido')
                            listamarca.append('desconhecida')
                            listacat.append('desconhecida')
                            listasubcat.append('desconhecida')
                            listaimg.append('desconhecida')
                            break
                else:
                    print('ERROR: A URL NÃO FOI TRATADA! Por favor, trate a url {} antes de executar o script'.format(url))
    else:
        nomesprodutos.append('-')
        listamarca.append('-')
        listacat.append('-')
        listasubcat.append('-')
        listaimg.append('-')
    #print('COD: {}'.format(listacod[ll]))
    #print('Produto: {}'.format(nomesprodutos[ll]))
    #print('Marca: {}'.format(listamarca[ll]))
    #print('Categoria: {}'.format(listacat[ll]))
    #print('Subcategoria: {}'.format(listasubcat[ll]))
    #print('Imagem: {}'.format(listaimg[ll]))
    #ll += 1

print('FECHANDO O NAVEGADOR!')
driver.close()

#GRAVANDO EM UMA NOVA PLANILHA
print('CRIANDO UMA NOVA PLANILHA...')
# 1. cria o arquivo
f = open('csv/Resultado.csv', 'w', newline='', encoding='utf-8')

# 2. cria o objeto de gravação
w = csv.writer(f)

print('Escrevendo na planilha criada')
#escreve a primeira linha
w.writerow(['EAN/GTIN','TITULO','MARCA','CATEGORIA','SUB-CATEGORIA','IMAGE'])
for i in range(len(listacod)):
    #escreve as proximas linhas
    w.writerow([listacod[i],nomesprodutos[i],listamarca[i],listacat[i],listasubcat[i],listaimg[i]])

print('Planilha criada e escrita!')

"""
#RESULTADO DAS LISTAS
for linha in range(len(listacod)):
    print('COD: {}'.format(listacod[linha]))
    print('Produto: {}'.format(nomesprodutos[linha]))
    print('Marca: {}'.format(listamarca[linha]))
    print('Categoria: {}'.format(listacat[linha]))
    print('Subcategoria: {}'.format(listasubcat[linha]))
    print('Imagem: {}'.format(listaimg[linha]))


              
#opções de configuração do navegador, para não mostrar que é uma automatização
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#abre o navegador, com as opções carregadas
driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options)


#navega o 1º site de busca da lista
for urlbusca in urslbusca:
    try:
        #driver.get('https://www.google.com/')
        driver.get(urlbusca)
    except:
        print('ERROR: Não foi possivel acessar a URL: {}'.format(urlbusca))
        print('Acessando o próximo site...')
        #driver.close()
        #exit()
    else:
        time.sleep(5)
        break
"""



"""              
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
                print('ERROR: Não foi possivel capturar')
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
                    subcat = 'DESCONHECIDA'
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
            listasubcat.append(subcat)
            listaimg.append(img)
        else:
            #senao tem codigo de barras, armazena '-' em todos os dados desejados
            nomesprodutos.append('-')
            listacod.append('-')
            listacat.append('-')
            listasubcat.append('-')
            listaimg.append('-')
        print('COD: {}'.format(listacod[linha-1]))
        print('Produto: {}'.format(nomesprodutos[linha-1]))
        print('Categoria: {}'.format(listacat[linha-1]))
        print('Subcategoria: {}'.format(listasubcat[linha - 1]))
        print('Imagem: {}'.format(listaimg[linha-1]))
        linha += 1
"""

"""
#GRAVANDO EM UMA NOVA PLANILHA
# 1. cria o arquivo
f = open('csv/Resultado.csv', 'w', newline='', encoding='utf-8')

# 2. cria o objeto de gravação
w = csv.writer(f)

#escreve a primeira linha
w.writerow(['EAN/GTIN','TITULO','CATEGORIA','IMAGE'])
for i in range(len(listacod)):
    #escreve as proximas linhas
    w.writerow([listacod[i],nomesprodutos[i],listacat[i],listaimg[i]])
"""