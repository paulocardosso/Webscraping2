# Projeto Webscraping Usando Python/Selenium

## Requisitos:

1. Python 3.6.3
    1. https://www.python.org/downloads/release/python-363/
1. Selenium 3.141.0
    1. https://selenium-python.readthedocs.io/installation.html
1. Driver (navegador)*
    1. https://www.selenium.dev/pt-br/documentation/webdriver/getting_started/install_drivers/


## Funcionamento:

1. O script2.py vai realizar o processo de leitura de um arquivo csv que está na pasta csv,
capturando todos os códigos de barras (presentes na 5º coluna), cada código de barra será 
verificado caso ele exista, fazendo as seguintes ações:
    1. Realizar busca do código de barras na Amazon
    1. Acessar o primeiro produto encontrado pela Amazon, caso exista
    1. Capturar o nome, a marca, a categoria, a subcategoria e a imagem do produto
    1. Armazenar cada atributo em cada array
1. Caso o código de barras não exista na Amazon, será procurado pelo mesmo no Google.
    1. Caso exista o código de barras pelo Google, o sistema acessará o site da Magazine Luiza
    1. Capturar o nome, a marca, a categoria, a subcategoria e a imagem do produto
    1. Armazenar cada atributo em cada array
1. Caso não exista na Amazon e nem no Google, será atribuido o valor desconhecido para todos 
os atributos desejados.
1. Após obter todos os dados desejados, de todos os códigos de barras, o script irá criar
um novo arquivo .csv com todos os resultados, incluindo o código que foi utilizado.

## Melhorias

O script em questão, vai gerá várias categorias e subcategorias diferentes de produtos que
pertencem a mesma categoria e subcategoria, como é o caso do produto: Pisca Pisca...
Uma possivel solução seria automatizar o processo de classificação dos produtos, com base
nos produtos já existentes e classificados. Além disso, os sites informado têm sistema de
bloqueio de automatização, portanto, erros poderão acontecer no script.