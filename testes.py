import csv

def atribuirlista(variavel,lista:list):
    if variavel:
        lista.append(variavel)
    else:
        lista.append('-')

#LEITURA DO CÓDIGO DE BARRAS DO ARQUIVO CSV
print('REALIZANDO A LEITURA DA PLANILHA...')
listacode = []
listafab = []
listadesc = []
listaun = []
listaean = []
listaqnt = []
listavalor = []
listacontarnome = []
listacontarbarcode = []

#Quantidade,Valor,Contar Nome,Contar Barcode
with open('csv/ListadeProdutos.csv', encoding='utf-8') as arquivo_referencia:
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
        atribuirlista(l[0], listacode)
        atribuirlista(l[1], listafab)
        atribuirlista(l[2], listadesc)
        atribuirlista(l[3], listaun)
        atribuirlista(l[4], listaean)
        atribuirlista(l[5], listaqnt)
        atribuirlista(l[6], listavalor)
        atribuirlista(l[7], listacontarnome)
        atribuirlista(l[8], listacontarbarcode)

print('LEITURA DA PLANILHA CONCLUÍDA')

#GRAVANDO EM UMA NOVA PLANILHA
print('CRIANDO UMA NOVA PLANILHA...')
# 1. cria o arquivo
f = open('csv/Resultado.csv', 'w', newline='', encoding='utf-8')

# 2. cria o objeto de gravação
w = csv.writer(f)

print('Escrevendo na planilha criada')
#escreve a primeira linha
w.writerow(['Código','Fabricante','Descricao dos Produtos','UN','EAN/GTIN','Quantidade','Valor','Contar Nome','Contar Barcode'])
for i in range(len(listaean)):
    #escreve as proximas linhas
    w.writerow([listacode[i],listafab[i],listadesc[i],listaun[i],listaean[i],listaqnt[i],listavalor[i],listacontarnome[i],listacontarbarcode[i]])