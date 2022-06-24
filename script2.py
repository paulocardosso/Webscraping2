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
#print(len(listacod))

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
urlsbusca = ['https://www.amazon.com.br/','https://www.lleferragens.com.br/','https://www.google.com.br/']

#ll = 0
check = False
#ACESSANDO OS SITES DE BUSCAS, REALIZANDO A BUSCA E TRAZENDO AS INFORMAÇÕES NECESSÁRIAS
print('GERANDO O RESULTADO...')
for cod in listacod:
    #caso exista codigo de barras e não seja SEM GTIN, realizar a operação de buscar informações
    if cod and not 'SEM GTIN' in cod and not '-' in cod:
        for url in urlsbusca:
            #vai acessar todas as urls de buscas presente na lista urlsbusca
            try:
                if 'lleferragens.com.br' in url:
                    try:
                        driver.get('https://www.lleferragens.com.br/produtos?search={}'.format(cod))
                    except:
                        continue
                    else:
                        time.sleep(2)
                        if not check:
                            input('Digite ENTER se fechou o chat e aceitou os cookies')
                            check = True
                else:
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
                #time.sleep(1)
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
                        # remover dados da url para pegar a categoria
                        time.sleep(3)
                        try:
                            amazon = driver.current_url
                        except:
                            continue
                        else:
                            sitecat = amazon.split('ref=')[0]
                            try:
                                driver.get(sitecat)
                            except:
                                continue
                            else:
                                time.sleep(3)
                        #se ter resultado, capturar os atributos do produto
                        try:
                            nameproduto = driver.find_element_by_xpath('//*[@id="productTitle"]').text
                        except:
                            continue
                        try:
                            marca = driver.find_element_by_xpath('//*[@id="productDetails_techSpec_section_1"]/tbody/tr[1]').text
                        except:
                            continue
                        else:
                            if 'Fabricante' in marca:
                                marca = marca.split('Fabricante ')[1]
                            elif 'marca' in marca:
                                marca = marca.split('marca ')[1]
                            else:
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
                            #img = 'indisponivel'
                        try:
                            categorias = driver.find_elements_by_xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li/span/a')
                        except:
                            continue
                        else:
                            if categorias:
                                cat = categorias[0].text
                                subcat = categorias[len(categorias) - 1].text
                                if subcat == '':
                                    subcat = 'indisponivel'
                            else:
                                cat = 'indisponivel'
                                subcat = 'indisponivel'
                        try:
                            reais = driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span/span[2]/span[2]').text
                            centavos = driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span/span[2]/span[3]').text
                        except:
                            try:
                                valor = driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span/span[2]').text
                            except:
                                continue
                            else:
                                valor = valor.replace('R$','')
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
                elif 'lleferragens.com.br' in url:
                    try:
                        res = driver.find_element_by_xpath('//div[@id="__next"]//div[@class="color-primary text-center fw-bold"]').text
                    except:
                        # tem produto
                        try:
                            driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div').click()
                        except:
                            continue
                        else:
                            time.sleep(3)
                    else:
                        #nao tem o produto
                        continue
                    try:
                        nameproduto = driver.find_element_by_xpath('//*[@id="__next"]//h2').text
                    except:
                        continue
                    else:
                        nome = nameproduto.split(' - ')
                        nameproduto = '{} - {}'.format(nome[0], nome[len(nome) - 1])
                        marca = nome[1]
                    try:
                        cat = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]').text
                    except:
                        continue
                    else:
                        cat = cat.split(': ')[1]
                    try:
                        subcat = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div[2]').text
                    except:
                        continue
                    else:
                        subcat = subcat.split(': ')[1]
                    try:
                        img = driver.find_element_by_xpath('//img[@class="image-gallery-image"]').get_attribute('src')
                    except:
                        continue
                    valor = 'indisponivel'
                    try:
                        site = driver.current_url
                    except:
                        continue
                    # adicionar os atributos nas listas
                    nomesprodutos.append(nameproduto)
                    listamarca.append(marca)
                    listacat.append(cat)
                    listasubcat.append(subcat)
                    listaimg.append(img)
                    listavalor.append(valor)
                    listaorigem.append(site)
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
                        resul = driver.find_element_by_xpath('//*[@id="rso"]/div/div/div/div/div[1]').text
                    except:
                        print('ERROR nao encontrou resul')
                        nomesprodutos.append('desconhecido')
                        listamarca.append('desconhecida')
                        listacat.append('desconhecida')
                        listasubcat.append('desconhecida')
                        listaimg.append('desconhecida')
                        listavalor.append('desconhecido')
                        listaorigem.append('desconhecida')
                        break
                    else:
                        if 'Sua pesquisa não encontrou' in resul:
                            nomesprodutos.append('desconhecido')
                            listamarca.append('desconhecida')
                            listacat.append('desconhecida')
                            listasubcat.append('desconhecida')
                            listaimg.append('desconhecida')
                            listavalor.append('desconhecido')
                            listaorigem.append('desconhecida')
                            break
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
                        link1 = ''
                        for link in elementos:
                            try:
                                link1 = link.get_attribute('href')
                            except:
                                link1 = ''
                                break
                            else:
                                if 'www.amazon.com.br' in link1:
                                    try:
                                        driver.get(link1)
                                    except:
                                        continue
                                    else:
                                        time.sleep(2)
                                    #continuar aqui
                                    try:
                                        nameproduto = driver.find_element_by_xpath('//*[@id="productTitle"]').text
                                    except:
                                        continue
                                    try:
                                        marca = driver.find_element_by_xpath('//*[@id="productDetails_techSpec_section_1"]/tbody/tr[1]').text
                                    except:
                                        continue
                                    else:
                                        if 'Fabricante' in marca:
                                            marca = marca.split('Fabricante ')[1]
                                        elif 'marca' in marca:
                                            marca = marca.split('marca ')[1]
                                        else:
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
                                        #img = 'indisponivel'
                                    try:
                                        categorias = driver.find_elements_by_xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li/span/a')
                                    except:
                                        continue
                                    else:
                                        if categorias:
                                            cat = categorias[0].text
                                            subcat = categorias[len(categorias) - 1].text
                                            if subcat == '':
                                                subcat = 'indisponivel'
                                        else:
                                            cat = 'indisponivel'
                                            subcat = 'indisponivel'
                                    try:
                                        reais = driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span/span[2]/span[2]').text
                                        centavos = driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span/span[2]/span[3]').text
                                    except:
                                        try:
                                            valor = driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span/span[2]').text
                                        except:
                                            try:
                                                valor = driver.find_element_by_xpath('//*[@id="outOfStock"]/div/div[1]/span[1]').text
                                            except:
                                                continue
                                            else:
                                                if 'Não' in valor:
                                                    valor = 'indisponivel'
                                        else:
                                            valor = valor.replace('R$', '')
                                    else:
                                        valor = '{},{}'.format(reais, centavos)
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
                                elif 'www.magazineluiza.com.br' in link1:
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
                                    time.sleep(2)
                                    # capturar as informações desejadas do site
                                    try:
                                        nameproduto = driver.find_element_by_xpath(
                                            '//*[@data-testid="heading-product-title"]').text
                                    except:
                                        continue
                                    else:
                                        if ' - ' in nameproduto:
                                            nameproduto = nameproduto.split(' - ')[0]
                                    try:
                                        marca = driver.find_element_by_xpath('//*[@data-testid="heading-product-brand"]').text
                                    except:
                                        continue
                                    try:
                                        img = driver.find_element_by_xpath('//img[@data-testid="image-selected-thumbnail"]').get_attribute('src')
                                    except:
                                        continue
                                        #img = 'indisponivel'
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
                                        time.sleep(3)
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
                                        continue
                                        #img = 'indisponivel'
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

#print(len(listacod))
#print(len(nomesprodutos))
#print(len(listamarca))
#print(len(listacat))
#print(len(listasubcat))
#print(len(listaimg))
#print(len(listaorigem))


#GRAVANDO EM UMA NOVA PLANILHA
print('CRIANDO UMA NOVA PLANILHA...')
# 1. cria o arquivo
f = open('csv/Resultado3.csv', 'w', newline='', encoding='utf-8')

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