import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#OPÇÕES DE CONFIGURAÇÃO DO NAVEGADOR
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#ABRIR O NAVEGADOR, COM AS CONFIGURAÇÕES AJUSTADAS ANTERIORMENTE
driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options)
driver.get('https://www.google.com.br')
time.sleep(5)

#driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()


input_busca = driver.find_element_by_xpath('//input[@name="q"]')
input_busca.clear()
input_busca.send_keys('7899432885551' + Keys.ENTER)
time.sleep(3)

#driver.find_element_by_xpath('//*[@id="rso"]//div//h3').click()
#time.sleep(3)

elementos = driver.find_elements_by_xpath('//*[@id="rso"]//div//a')
linkmagalu = ''
for link in elementos:
    if 'magazineluiza.com.br' in link.get_attribute('href'):
        linkmagalu = link.get_attribute('href')
        break
if linkmagalu != '':
    driver.get(linkmagalu)
    time.sleep(5)

try:
    driver.find_element_by_xpath('//button[@data-testid="button-message-box"]').click()
except:
    print('Ja aceitou os cookies')
else:
    time.sleep(1)
    driver.find_element_by_xpath('//div[@class="container-button-banner"]').click()
    time.sleep(1)

nameproduto = driver.find_element_by_xpath('//*[@data-testid="heading-product-title"]').text
nameproduto = nameproduto.split(' - ')[0]
marca = driver.find_element_by_xpath('//*[@data-testid="heading-product-brand"]').text
img = driver.find_element_by_xpath('//img[@data-testid="image-selected-thumbnail"]').get_attribute('src')
categorias = driver.find_elements_by_xpath('//*[@data-testid="breadcrumb-item-list"]')
cat = categorias[2].text
subcat = categorias[3].text



#driver.find_element_by_xpath('//img[@class="s-image"]').click()

#nameproduto = driver.find_element_by_xpath('//*[@id="productTitle"]').text
#marca = driver.find_element_by_xpath('//*[@id="bylineInfo"]').text
#marca = marca.split(':')[1].strip()
#img = driver.find_element_by_xpath('//*[@id="landingImage"]').get_attribute('src')
#elementos = driver.find_elements_by_xpath('//*[@id="nav-subnav"]/a')
#cat = elementos[0].text
#subcat = elementos[len(elementos)-1].text

print(nameproduto)
print(marca)
print(img)
print(cat)
print(subcat)

"""
                elif 'telhanorte.com.br' in url:
                    #aceitar os cookies da pagina, caso exista essa opção, senão apenas pula
                    try:
                        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                    except:
                        pass

                    # buscar o produto pelo codigo
                    input_busca = driver.find_element_by_xpath('//*[@id="chaordicSearch"]')
                    input_busca.clear()
                    input_busca.send_keys(cod + Keys.ENTER)
                    time.sleep(3)

                    # verificar se encontrou o resultado
                    try:
                        resul = driver.find_element_by_xpath('//p[@class="x-category__product-qty"]').text
                    except:
                        # senao encontrou pular para o proximo site de busca
                        continue
                    else:
                        #caso encontre, retornará apenas um produto, pois o código de barras é único
                        if '1 produto' in resul:
                            #acessa a pagina do produto encontrado
                            driver.find_element_by_xpath('//a[@class="x-shelf__link"]').click()
                            time.sleep(3)

                            #capturar as informações desejadas, através do site aberto
                            nameproduto = driver.find_element_by_xpath('//h1[@rv-text="state.productName"]').text
                            marca = nameproduto.split(' ')
                            marca = marca[len(marca)-1]
                            img = driver.find_element_by_xpath('//*[@id="productImage"]').get_attribute('src')
                            categorias = driver.find_elements_by_xpath('//li[@itemprop]')
                            cat = categorias[1].text
                            subcat = driver.find_element_by_xpath('//li[@class="last"]').text

                            #adicionar as informações obtidas anteriormente, nas listas
                            nomesprodutos.append(nameproduto)
                            listamarca.append(marca)
                            listacat.append(cat)
                            listasubcat.append(subcat)
                            listaimg.append(img)

                            #parar o loop de urls de buscas
                            break
                """