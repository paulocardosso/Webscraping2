import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#LEITURA DO CÓDIGO DE BARRAS DO ARQUIVO CSV
print('REALIZANDO A LEITURA DA PLANILHA...')
listacod = []
with open('csv/ListadeProdutosVal2.csv', encoding='utf-8') as arquivo_referencia:
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
        cod = l[0]
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
listavalor = []
listaorigem = []

#OPÇÕES DE CONFIGURAÇÃO DO NAVEGADOR
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#ABRIR O NAVEGADOR, COM AS CONFIGURAÇÕES AJUSTADAS ANTERIORMENTE
print('ABRINDO O NAVEGADOR')
driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options)

#URLS DE BUSCAS DE PRODUTOS
urlsbusca = ['https://www.amazon.com.br/','https://www.google.com.br/']

#ll = 0
#ACESSANDO OS SITES DE BUSCAS, REALIZANDO A BUSCA E TRAZENDO AS INFORMAÇÕES NECESSÁRIAS
print('GERANDO O RESULTADO...')
for cod in listacod:
    #caso exista codigo de barras e não seja SEM GTIN, realizar a operação de buscar informações
    if cod and not 'SEM GTIN' in cod and not '-' in cod:
        for url in urlsbusca:
            #vai acessar todas as urls de buscas presente na lista urlsbusca
            try:
                driver.get(url)
            except:
                #senao conseguiu acessar, vai exibir e pular para o proximo site
                print('ERROR: Não foi possivel acessar a URL: {}'.format(url))
                if url == 'https://www.google.com.br/':
                    print('PARADA OBRIGATÓRIA! Por favor, verifique a conexão e reinicie a execução do script')
                    nomesprodutos.append('desconhecido')
                    listamarca.append('desconhecida')
                    listacat.append('desconhecida')
                    listasubcat.append('desconhecida')
                    listaimg.append('desconhecida')
                    listavalor.append('desconhecido')
                    listaorigem.append('desconhecida')
                    break
                else:
                    continue
            else:
                # Tempo para carregar o presente site
                time.sleep(3)
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
                        resultxt = driver.find_element_by_xpath('//div[@class="a-section a-spacing-small a-spacing-top-small"]').text
                    except:
                        continue
                    else:
                        if not '1 resultado' in resultxt:
                            continue
                    try:
                        driver.find_element_by_xpath('//img[@class="s-image"]').click()
                    except:
                        #senao ter imagem, não encontrou o resultado, buscar no proximo site
                        continue
                    else:
                        #se ter resultado, capturar os atributos do produto
                        try:
                            nameproduto = driver.find_element_by_xpath('//*[@id="productTitle"]').text
                        except:
                            continue
                        try:
                            marca = driver.find_element_by_xpath('//*[@id="bylineInfo"]').text
                        except:
                            continue
                        else:
                            if ':' in marca:
                                marca = marca.split(':')[1].strip()
                        try:
                            img = driver.find_element_by_xpath('//*[@id="landingImage"]').get_attribute('src')
                        except:
                            continue
                        try:
                            categorias = driver.find_elements_by_xpath('//*[@id="nav-subnav"]/a')
                        except:
                            continue
                        else:
                            cat = categorias[0].text
                            subcat = categorias[len(categorias)-1].text
                        if subcat == '':
                            subcat = 'null'
                        try:
                            reais = driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span/span[2]/span[2]').text
                            centavos = driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span/span[2]/span[3]').text
                        except:
                            continue
                        else:
                            valor = '{},{}'.format(reais,centavos)
                        try:
                            site = driver.current_url
                        except:
                            continue
                        #adicionar os atributos nas listas
                        nomesprodutos.append(nameproduto)
                        listamarca.append(marca)
                        listacat.append(cat)
                        listasubcat.append(subcat)
                        listaimg.append(img)
                        listavalor.append(valor)
                        listaorigem.append(site)
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
                        listavalor.append('desconhecido')
                        listaorigem.append('desconhecida')
                        break
                    else:
                        input_busca.clear()
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
                        listavalor.append('desconhecido')
                        listaorigem.append('desconhecida')
                        break
                    else:
                        time.sleep(3)
                        link1 = ''
                        for link in elementos:
                            try:
                                link1 = link.get_attribute('href')
                            except:
                                link1 = ''
                                break
                            else:
                                if 'www.magazineluiza.com.br' in link1:
                                    try:
                                        driver.get(link1)
                                    except:
                                        continue
                                    else:
                                        time.sleep(5)
                                    # aceitar os cookies
                                    try:
                                        driver.find_element_by_xpath('//button[@data-testid="button-message-box"]').click()
                                    except:
                                        pass
                                    else:
                                        time.sleep(1)
                                        try:
                                            driver.find_element_by_xpath('//div[@class="container-button-banner"]').click()
                                        except:
                                            pass
                                    time.sleep(5)
                                    # capturar as informações desejadas do site
                                    try:
                                        nameproduto = driver.find_element_by_xpath(
                                            '//*[@data-testid="heading-product-title"]').text
                                    except:
                                        continue
                                    else:
                                        nameproduto = nameproduto.split(' - ')[0]
                                    try:
                                        marca = driver.find_element_by_xpath('//*[@data-testid="heading-product-brand"]').text
                                    except:
                                        continue
                                    try:
                                        img = driver.find_element_by_xpath('//img[@data-testid="image-selected-thumbnail"]').get_attribute('src')
                                    except:
                                        continue
                                    try:
                                        categorias = driver.find_elements_by_xpath('//*[@data-testid="breadcrumb-item-list"]')
                                    except:
                                        continue
                                    else:
                                        try:
                                            cat = categorias[2].text
                                            subcat = categorias[3].text
                                        except:
                                            continue
                                    try:
                                        valor = driver.find_element_by_xpath('//*[@data-testid="price-value"]').text
                                    except:
                                        continue
                                    try:
                                        site = driver.current_url
                                    except:
                                        continue
                                    # adicionar as informações obtidas nas listas
                                    nomesprodutos.append(nameproduto)
                                    listamarca.append(marca)
                                    listacat.append(cat)
                                    listasubcat.append(subcat)
                                    listaimg.append(img)
                                    listavalor.append(valor)
                                    listaorigem.append(site)
                                    break
                                elif 'www.americanas.com.br' in link1:
                                    try:
                                        driver.get(link1)
                                    except:
                                        continue
                                    else:
                                        time.sleep(6)
                                    #aceitar os cookies da amarecinas, para evitar bloqueio
                                    try:
                                        driver.find_element_by_xpath('//*[@id="rsyswpsdk"]/div/header/div[2]/button').click()
                                    except:
                                        pass
                                    try:
                                        nameproduto = driver.find_element_by_xpath('//*[@id="rsyswpsdk"]//h1').text
                                    except:
                                        continue
                                    try:
                                        marca = driver.find_element_by_xpath('//*[@id="rsyswpsdk"]/div/main/div[6]/div[2]/div/div[2]/table/tbody/tr[3]/td[2]').text
                                    except:
                                        try:
                                            marca = driver.find_element_by_xpath('//*[@id="rsyswpsdk"]/div/main/div[7]/div[2]/div/div[2]/table/tbody/tr[3]/td[2]').text
                                        except:
                                            continue
                                    if not marca:
                                        marca = 'indisponivel'
                                    try:
                                        img = driver.find_element_by_xpath('//*[@id="rsyswpsdk"]/div/div/div/div/div/div/a/div/div/picture/img').get_attribute('src')
                                    except:
                                        continue
                                    try:
                                        categorias = driver.find_elements_by_xpath('//*[@id="rsyswpsdk"]/div/main/div[1]/div/ul/li')
                                    except:
                                        continue
                                    else:
                                        try:
                                            cat = categorias[1].text
                                            subcat = categorias[len(categorias) - 1].text
                                        except:
                                            continue
                                    try:
                                        valor = driver.find_element_by_xpath('//*[@id="rsyswpsdk"]/div/main/div[2]/div[2]/div[1]/div[1]/div').text
                                    except:
                                        valor = 'indisponivel'
                                    try:
                                        site = driver.current_url
                                    except:
                                        continue
                                    # adicionar as informações obtidas nas listas
                                    nomesprodutos.append(nameproduto)
                                    listamarca.append(marca)
                                    listacat.append(cat)
                                    listasubcat.append(subcat)
                                    listaimg.append(img)
                                    listavalor.append(valor)
                                    listaorigem.append(site)
                                    break
                                elif 'www.ocompra.com' in link1:
                                    try:
                                        driver.get(link1)
                                    except:
                                        nomesprodutos.append('desconhecido')
                                        listamarca.append('desconhecida')
                                        listacat.append('desconhecida')
                                        listasubcat.append('desconhecida')
                                        listaimg.append('desconhecida')
                                        listavalor.append('desconhecido')
                                        listaorigem.append('desconhecida')
                                        break
                                    else:
                                        time.sleep(5)
                                    try:
                                        nameproduto = driver.find_element_by_xpath('/html/body/div[1]/h1').text
                                    except:
                                        nomesprodutos.append('desconhecido')
                                        listamarca.append('desconhecida')
                                        listacat.append('desconhecida')
                                        listasubcat.append('desconhecida')
                                        listaimg.append('desconhecida')
                                        listavalor.append('desconhecido')
                                        listaorigem.append('desconhecida')
                                        break
                                    try:
                                        marca = driver.find_element_by_xpath('/html/body/div[1]/div[6]/h2[1]/span').text
                                    except:
                                        nomesprodutos.append('desconhecido')
                                        listamarca.append('desconhecida')
                                        listacat.append('desconhecida')
                                        listasubcat.append('desconhecida')
                                        listaimg.append('desconhecida')
                                        listavalor.append('desconhecido')
                                        listaorigem.append('desconhecida')
                                        break
                                    try:
                                        img = driver.find_element_by_xpath('//img[@class="miniImg"]').get_attribute('src')
                                    except:
                                        nomesprodutos.append('desconhecido')
                                        listamarca.append('desconhecida')
                                        listacat.append('desconhecida')
                                        listasubcat.append('desconhecida')
                                        listaimg.append('desconhecida')
                                        listavalor.append('desconhecido')
                                        listaorigem.append('desconhecida')
                                        break
                                    try:
                                        categorias = driver.find_elements_by_xpath('//a[@class="semDecoracao"]')
                                    except:
                                        nomesprodutos.append('desconhecido')
                                        listamarca.append('desconhecida')
                                        listacat.append('desconhecida')
                                        listasubcat.append('desconhecida')
                                        listaimg.append('desconhecida')
                                        listavalor.append('desconhecido')
                                        listaorigem.append('desconhecida')
                                        break
                                    else:
                                        try:
                                            cat = categorias[1].text
                                            subcat = categorias[len(categorias) - 1].text
                                        except:
                                            nomesprodutos.append('desconhecido')
                                            listamarca.append('desconhecida')
                                            listacat.append('desconhecida')
                                            listasubcat.append('desconhecida')
                                            listaimg.append('desconhecida')
                                            listavalor.append('desconhecido')
                                            listaorigem.append('desconhecida')
                                            break
                                    valor = 'indisponivel'
                                    try:
                                        site = driver.current_url
                                    except:
                                        nomesprodutos.append('desconhecido')
                                        listamarca.append('desconhecida')
                                        listacat.append('desconhecida')
                                        listasubcat.append('desconhecida')
                                        listaimg.append('desconhecida')
                                        listavalor.append('desconhecido')
                                        listaorigem.append('desconhecida')
                                        break
                                    # adicionar as informações obtidas nas listas
                                    nomesprodutos.append(nameproduto)
                                    listamarca.append(marca)
                                    listacat.append(cat)
                                    listasubcat.append(subcat)
                                    listaimg.append(img)
                                    listavalor.append(valor)
                                    listaorigem.append(site)
                                    break
                                else:
                                    link1 = ''
                        if link1 != '':
                            break
                        else:
                            nomesprodutos.append('desconhecido')
                            listamarca.append('desconhecida')
                            listacat.append('desconhecida')
                            listasubcat.append('desconhecida')
                            listaimg.append('desconhecida')
                            listavalor.append('desconhecido')
                            listaorigem.append('desconhecida')
                            break
                else:
                    print('ERROR: A URL NÃO FOI TRATADA! Por favor, trate a url {} antes de executar o script'.format(url))
    else:
        nomesprodutos.append('-')
        listamarca.append('-')
        listacat.append('-')
        listasubcat.append('-')
        listaimg.append('-')
        listavalor.append('-')
        listaorigem.append('-')
    #print('COD: {}'.format(listacod[ll]))
    #print('Produto: {}'.format(nomesprodutos[ll]))
    #print('Marca: {}'.format(listamarca[ll]))
    #print('Categoria: {}'.format(listacat[ll]))
    #print('Subcategoria: {}'.format(listasubcat[ll]))
    #print('Imagem: {}'.format(listaimg[ll]))
    #print('Valor: {}'.format(listavalor[ll]))
    #print('Origem: {}'.format(listaorigem[ll]))
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
w.writerow(['EAN/GTIN','TITULO','MARCA','CATEGORIA','SUB-CATEGORIA','IMAGE','VALOR','ORIGEM'])
for i in range(len(listacod)):
    #escreve as proximas linhas
    #acrescentar valor e origem
    w.writerow([listacod[i],nomesprodutos[i],listamarca[i],listacat[i],listasubcat[i],listaimg[i],listavalor[i],listaorigem[i]])

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