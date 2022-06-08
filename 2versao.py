import csv
import os
import urllib.request
import time
from selenium import webdriver

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
