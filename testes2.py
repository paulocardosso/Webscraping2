import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#OPÇÕES DE CONFIGURAÇÃO DO NAVEGADOR
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#ABRIR O NAVEGADOR, COM AS CONFIGURAÇÕES AJUSTADAS ANTERIORMENTE
driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options)
check = False
cod = ['2000000000107','1789605030174','2000000053820','2000000059167']
i = 0
while True:
    if i >= len(cod):
        driver.close()
        break
    driver.get('https://www.lleferragens.com.br/produtos?search={}'.format(cod[i]))
    i += 1
    time.sleep(5)
    if not check:
        input('Digite ENTER caso tenha fechado o chat e aceitado os cookies da página\n')
        check = True
    time.sleep(2)
    """
    try:
        input_busca = driver.find_element_by_xpath('//input[@placeholder="Buscar"]')
    except:
        continue
    else:
        input_busca.clear()        
        input_busca.send_keys(cod[i] + Keys.ENTER)
        time.sleep(5)
        i += 1
    """
    try:
        res = driver.find_element_by_xpath('//div[@id="__next"]//div[@class="color-primary text-center fw-bold"]').text
    except:
        #tem produto
        try:
            driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div').click()
        except:
            print('-')
            print('-')
            print('-')
            print('-')
            print('-')
            print('-')
            print('-')
            continue
        else:
            time.sleep(5)
    else:
        print('-')
        print('-')
        print('-')
        print('-')
        print('-')
        print('-')
        print('-')
        continue
    try:
        nameproduto = driver.find_element_by_xpath('//*[@id="__next"]//h2').text
    except:
        continue
    else:
        nome = nameproduto.split(' - ')
        nameproduto = '{} - {}'.format(nome[0],nome[len(nome)-1])
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
    print(nameproduto)
    print(marca)
    print(img)
    print(cat)
    print(subcat)
    print(valor)
    print(site)



"""
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
"""

#print(nameproduto)
#print(marca)
#print(img)
#print(cat)
#print(subcat)