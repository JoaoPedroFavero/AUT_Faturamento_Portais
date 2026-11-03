import pyautogui as pag, pytesseract as pyt, os, time, pymsgbox, pandas, glob, re, sys
import sqlPython, funcoesMain
from dataclasses import dataclass

import os
from dotenv import load_dotenv
load_dotenv()

# ✅ ❌🤖

pyt.tesseract_cmd = os.getenv("PYTESSERACT_LOCAL")

@dataclass(frozen=True)
class Constante:
    PORTAL_SCHULZ: str = os.getenv("PORTAL")
    DIM: str = os.getenv("SISTEMA")
    CNPJ_SCHULZ_COMPRESSORES: str = os.getenv("CNPJ")
constante = Constante()

#C:\Users\USER\Downloads #path para o Excel da Schulz

def alertaPag(msg, pagFail):
    print(msg, pagFail)
    pymsgbox.alert(msg)
    sys.exit()

def alertaException(msg, erro):
    print(msg, erro)
    pymsgbox.alert(msg)
    sys.exit()

def alertaElse(msg):
    print(msg)
    pymsgbox.alert(msg)
    sys.exit()

pag.PAUSE = 1.2

#PROCURANDO CHROME
posChrome = pag.locateOnScreen(r"imagensOCR\chrome.png", confidence = 0.9)
try:
    if(posChrome):
        pag.click(posChrome)
        print("✅ Chrome encontrado!")
    else:
        print("❌ Chrome não encontrado!")
except Exception as erro:
    print("Erro:", erro)

#PROCURANDO '+' PARA GERAR NOVA GUIA e PROCURANDO BARRA DE PESQUISA
funcoesMain.novaGuiaChrome()

#ENTRANDO NO PORTAL DA SCHULZ
try:
    pag.write(constante.PORTAL_SCHULZ)
    pag.press("enter")
except pag.FailSafeException as pagFail:
    alertaPag("Encerrado por PyAutoGui de forma Segura", pagFail)

#ENTRANDO/LOGANOD NO PORTAL
try:
    posEntrarPortalSchulz = pag.locateOnScreen(r"imagensOCR\entrarPortalSchulz.png", confidence = 0.9)
except Exception as erro:
    print("🤖 Não foi possível encontrar o botão 'ENTRAR'! Verificando se já está logado")
    posEntrarPortalSchulz = None

try:
    if(posEntrarPortalSchulz != None):
        time.sleep(1)
        pag.click(posEntrarPortalSchulz)
        print("Entrando no portal da Schulz...")
        time.sleep(5)
        try:
            posConfirmacaoDeAcesso = pag.locateOnScreen(r"imagensOCR\confirmacaoDeAcesso.png", confidence=0.9)
        except Exception as erro:
            alertaException("Imagem de Confirmação de acesso não encontrada!", erro)
            posConfirmacaoDeAcesso = None
            print(type(posConfirmacaoDeAcesso))

        if(posConfirmacaoDeAcesso is not None):
            print("✅ Painel Schulz acessado com Sucesso!")

    elif(posEntrarPortalSchulz == None): #VERIFICANDO POSSIVEL LOGIN JÁ REALIZADO
        try:
            posPainelSchulz = pag.locateOnScreen(r"imagensOCR\painelSchulz.png", confidence = 0.8)
        except Exception as erro:
            posPainelSchulz = None
        cronometro = time.time() #utiliza a função time() da biblioteca time para contar quanto tempo dura uma tarefa

        while(posPainelSchulz == None and time.time() - cronometro < 10): #enqunato o posPainelSchulz não fo encontrado ele fica num loop de 5 segundos tentando encontrar. qunado encontra sai do loop
            try:
                posPainelSchulz = pag.locateOnScreen(r"imagensOCR\painelSchulz.png", confidence = 0.8)
            except:
                posPainelSchulz = None
            time.sleep(2)
            if(posPainelSchulz):
                break

        if(posPainelSchulz != None):
            print("✅ Painel Schulz já estava logado e foi acessado com Sucesso!")
    else:
        alertaElse("❌ Não foi possível acessar painel da Schulz...")
except Exception as error:
    alertaException("Ocorreu um erro no código:", error)
except pag.FailSafeException as pagFail:
    alertaPag("Encerrado por PyAutoGui", pagFail)

#IDENTIFICANDO EXCEL E CAPTANDO INFORMAÇÕES PARA FATURAMENTO
try:
    posBaixarExcelOC = pag.locateOnScreen(r"imagensOCR\baixarExcelOC.png", confidence = 0.8)
except Exception as erro:
    alertaException("Não foi possível encontrar o botão de Baixar Excel", erro)
    posBaixarExcelOC = None

if(posBaixarExcelOC):
    pag.click(posBaixarExcelOC)
    print("Encontrado botão para Download do Excel da OC...")
    time.sleep(0.5)
try:
    posConfirmacaoDownload = pag.locateOnScreen(r"imagensOCR\confirmacaoDownload.png", confidence = 0.8)
except:
    print("🤖 Download NÃO iniciado! Clicando novamente no botão!")
    posConfirmacaoDownload = None

if(posConfirmacaoDownload):
    print("Download do Excel da OC iniciado com sucesso. Será encaminhado para a Pasta Download")
    time.sleep(1)
else:
    tentativas = 0
    while(posConfirmacaoDownload == None and tentativas < 4):
        pag.click(posBaixarExcelOC)
        tentativas =+ 1
        time.sleep(0.5)
        try:
            posConfirmacaoDownload = pag.locateOnScreen(r"imagensOCR\confirmacaoDownload.png", confidence = 0.8)
        except:
            print(f"🤖 Download NÃO iniciado! Clicando novamente no botão pela {tentativas}° vez!")

        if(posConfirmacaoDownload):
            print("Download do Excel da OC iniciado com sucesso. Será encaminhado para a Pasta Download")
            time.sleep(1)
            break

pastaDownloads = os.path.join(os.path.expanduser("~"), "Downloads") #Caminho da Pasta Downloads - testado com print: Caminho correto.
todosArquivos = glob.glob(os.path.join(pastaDownloads, "*.xlsx")) #Lista TODOS (*) os arquivos .xlsx
planilhaMaisRecente = max(todosArquivos, key = os.path.getctime) #Lista o MAIS recente arquivo .xlsx

#print("Eis a planilha mais recente da pasta de Downloads:", planilhaMaisRecente)

ocSchulz = pandas.read_excel(planilhaMaisRecente)
# colunasImportantesOC = ["Item", "O.C.", "Qtd Ordem"]
listaItemOC = ocSchulz["Item"].to_list() #lista de todos os itens da Coluna Item
listaOrdemOC = ocSchulz["O.C."].to_list() #lista de todas as OCs da coluna O.C.
listaQtdOC = ocSchulz["Qtd Ordem"].to_list() #lista de todas as quantidades de itens da coluna Qtd Ordem

#NOVA GUIA PARA ACESSAR O DIM
funcoesMain.novaGuiaChrome()
pag.write(str(constante.DIM))
pag.press("enter")

#ACESSANDO O DIM
try:
    posAbaLoginDIM = pag.locateOnScreen(r"imagensOCR\abaLoginDIM.png", confidence = 0.9)
except:
    print("🤖 Não foi identificado o Painel de Login... Aguardarei para ver se já está logado.")
    posAbaLoginDIM = None

if(posAbaLoginDIM):
    try:
        posEntrarDimensao = pag.locateOnScreen(r"imagensOCR\entrarDimensao.png", confidence = 0.9)
    except:
        posEntrarDimensao = None

    try:
        if(posEntrarDimensao):
            pag.click(posEntrarDimensao)
            print("Entrando no Painel do Sistema Dimensão...")
            time.sleep(2)

            try:
                posDashboardDIM = pag.locateOnScreen(r"imagensOCR\dashboardDIM.png", confidence = 0.9)
            except Exception as erro:
                posDashboardDIM = None
                alertaException("❌ Não foi possivel localizar o Dashboard do Dimensão.", erro)

            if(posDashboardDIM is not None):
                print("✅ Painel do Dimensão acessado com sucesso!")
    except Exception as erro:
        alertaException("❌ Não foi encontrado o botão de 'Entrar' no Dimensão!", erro)

else:
    time.sleep(2)
    try:
        posDashboardDIM = pag.locateOnScreen(r"imagensOCR\dashboardDIM.png", confidence = 0.9)
    except Exception as erro:
        posDashboardDIM = None
    
    if(posDashboardDIM == None):
        contador = time.time()
        while(posDashboardDIM == None and time.time() - contador < 5):
            print(contador)
            try:
                posDashboardDIM = pag.locateOnScreen(r"imagensOCR\dashboardDIM.png", confidence = 0.9)
            except pag.FailSafeException as FailSafe:
                alertaPag("Finalizado por PyAutoGui FailSafe!", FailSafe)
                break
            except Exception as erro:
                posDashboardDIM = None
            time.sleep(1)

            if(posDashboardDIM is not None):
                print("✅ DIM já estava logado! Painel acessado com sucesso!")
                break
    else:
        print("✅ DIM já estava logado! Painel acessado com sucesso!")

#CONSULTAR ESTOQUE ANTES DE FATURAR
try:
    posAbaSuprimentos = pag.locateOnScreen(r"imagensOCR\abaSuprimentos.png", confidence = 0.9)
except Exception as erro:
    alertaException("❌ Não foi possível encontrar a aba Suprimentos no DIM.", erro)
    posAbaSuprimentos = None
    
listaItemFaturar = [] #Lista daqueles itens que TEM ESTOQUE e estão no Ranking para Faturamento!
if(posAbaSuprimentos):
    pag.click(posAbaSuprimentos)
    time.sleep(1)
    try:
        posAbaEstoque = pag.locateOnScreen(r"imagensOCR\abaEstoque.png", confidence = 0.9)
    except Exception as erro:
        alertaException("❌ Não foi possível encontrar a aba Estoque no DIM.", erro)
        posAbaEstoque = None

    if(posAbaEstoque):
        pag.click(posAbaEstoque)
        time.sleep(1)
        try:
            posAbaSaldos = pag.locateOnScreen(r"imagensOCR\abaSaldos.png", confidence = 0.9)
        except Exception as erro:
            alertaException("❌ Não foi possível encontrar a aba Saldos no DIM.", erro)
            posAbaSaldos = None

        if(posAbaSaldos):
            pag.click(posAbaSaldos)
            time.sleep(1)

        try:
            posBoxConsultaSaldo = pag.locateOnScreen(r"imagensOCR\boxConsultarSaldo.png" ,confidence = 0.9)
        except Exception as erro:
            posBoxConsultaSaldo = None
            alertaException("❌ Não foi possível encontrar o box de Consulta de Saldos no DIM.", erro)

        if(posBoxConsultaSaldo):
            for j in range(len(listaOrdemOC)):
                ordemCompra = listaOrdemOC[j]
                ocDiferente = False
                for i in range(len(listaItemOC)):
                    ordemCompraAtual = listaOrdemOC[i]

                    if(ordemCompraAtual == ordemCompra):
                        pag.click(posBoxConsultaSaldo)
                        time.sleep(0.5)
                        try:
                            codigoST = sqlPython.selecionarCodST(f""" SELECT codProdutosST FROM Contratos WHERE (codProdutosClientes = {listaItemOC[i]} and rankingProduto = 'A') """)
                        except Exception as erro:
                            alertaException("❌ Não foi possível conectar com PORTAIS_SOLTRONIC ou localizar o código de Rank 'A'.", erro)
                            break

                        pag.write(str(codigoST), interval = 1)
                        print(f"Código consultado: {str(codigoST)}")
                        pag.press("enter")

                        try:
                            posBotaoConsultar = pag.locateOnScreen(r"imagensOCR\botaoConsultar.png", confidence = 0.9)
                        except Exception as erro:
                            alertaException("❌ Não foi possível encontrar o Botão Consultar para consultar o saldo!")
                        
                        if(posBotaoConsultar):
                            pag.click(posBotaoConsultar)
                            time.sleep(0.6)

                        try:
                            time.sleep(3)
                            x, y, width, height = 594, 492, 100, 100
                            lerSaldo = pag.screenshot(region = (x, y, width, height))
                            lerSaldo.save("imagensOCR\lerSaldo.png")
                            imagemLida = pyt.image_to_string(lerSaldo, lang = "eng", config="--psm 6")

                            numeroLido = re.findall(r"\d+[.,]?\d*", imagemLida)
                            saldoTotal = float(numeroLido[0].replace(",", "."))
                        except Exception as erro:
                            alertaException("❌ Falha ao ler a quantidade Total do Item!", erro)
                            break

                        if(saldoTotal >= float(listaQtdOC[i])):
                            print("🤖 O Item rank 'A' TEM estoque o suficiente! Adicionando ele a Lista para Faturar!")
                            print(f"Quantidade em Saldo: {saldoTotal}")
                            listaItemFaturar.append(codigoST)
                            continue
                        else:
                            print("🤖 O Item rank 'A' NÃO TEM estoque o suficiente, testarei o de Rank 'B'!")
                            try:
                                codigoST = sqlPython.selecionarCodST(f""" SELECT codProdutosST FROM Contratos WHERE (codProdutosClientes = {listaItemOC[i]} and rankingProduto = 'B') """)
                            except Exception as erro:
                                alertaException("❌ Não foi possível conectar com PORTAIS_SOLTRONIC ou localizar o código de Rank 'B'.")
                                break

                            if(saldoTotal >= float(listaQtdOC[i])):
                                print("🤖 O Item rank 'B' TEM estoque o suficiente! Adicionando ele a Lista para Faturar!")
                                print(f"Quantidade em Saldo: {saldoTotal}")
                                listaItemFaturar.append(codigoST)
                                continue
                            else:
                                print("🤖 Não exite nenhum Código de Rank 'B' para esse produto!")
                                if(len(listaItemOC) > 1):
                                    continue
                                else:
                                    print(f"Não existem mais Produtos nessa Ordem de Compra: {ordemCompraAtual}")
                    else:
                        ocDiferente = True
                        break
                if(ocDiferente == True):
                    print(f"Ordem de Compra diferente encontrada! Faturando OC {ordemCompra}!")
                    break

print("🤖 Aqui esta(ão) o(s) item(ns) para faturar:", listaItemFaturar)


#ENTRANDO NA ABA DE VENDAS -> PEDIDOS/NF
try:
    posAbaVendas = pag.locateOnScreen(r"imagensOCR\simboloAbaVendas.png", confidence = 0.9)
except Exception as erro:
    alertaException("❌ Não foi possível encontrar a aba de Vendas no Dashboard do DIM!", erro)
    posAbaVendas = None

if(posAbaVendas):
    pag.click(posAbaVendas)
    print("Aba Vendas Encontrada... Prosseguindo para Pedidos/NF")
else:
    print("❌ Não foi possível encontrar a Aba Vendas...")

time.sleep(0.8)

try:
    posAbaPedidosNF = pag.locateOnScreen(r"imagensOCR\abaPedidosNF.png", confidence = 0.9)
except Exception as erro:
    alertaException("❌ Não foi possivel encontrar a aba Pedidos/NF no Dashboard do DIM!")
    posAbaPedidosNF = None

if(posAbaPedidosNF):
    pag.click(posAbaPedidosNF)
    print("Pedidos/NF encontrado! Seguindo para lançamento do Pedido!")
else:
    print("❌ Não foi possivel encontrar a aba 'Pedidos/NF' no DIM!")

# INICIANDO LANÇAMENTO DO PEDIDO
try:
    posBotaoLancar = pag.locateOnScreen(r"imagensOCR\botaoLancar.png", confidence = 0.9)
except Exception as erro:
    alertaException("❌ Não foi possivel encontrar botão de 'Lançar' no DIM!", erro)
    posBotaoLancar = None

if(posBotaoLancar):
    pag.click(posBotaoLancar)
    print("Iniciando Lançamento do Pedido no DIM");
else:
    print("❌ Não foi possível iniciar o lançamento de Pedidos no DIM!")

try:
    posConfirmacaoLancarPedido = pag.locateOnScreen(r"imagensOCR\confirmacaoLancarPedido.png", confidence = 0.9)
except Exception as erro:
    posConfirmacaoLancarPedido = None
    alertaException("❌ Erro ao encontrar Confirmação de aba de Lançamento!", erro)

if(posConfirmacaoLancarPedido):
    print("✅ Painel de Lançamento de Pedidos/NF acessado com sucesso e pronto!")
else:
    print("❌ Painel de Lançamento não foi acessado com êxito...")

#LANÇANDO CNPJ
try:
    posBoxSelecionarCliente = pag.locateOnScreen(r"imagensOCR\boxSelecionarCliente.png", confidence = 0.8)
except Exception as erro:
    alertaException("❌ Não foi possível encontrar o Box para Selecionar o Cliente.", erro)
    posBoxSelecionarCliente = None;

if(posBoxSelecionarCliente):
    pag.click(posBoxSelecionarCliente)
else:
    print("❌ Não foi possível clicar no Box de Selecionar Cliente.")

pag.write(str(constante.CNPJ_SCHULZ_COMPRESSORES))
time.sleep(1.5)
pag.press("enter")
'''
listaItemOC = ocSchulz["Item"].to_list() #lista de todos os itens da Coluna Item
listaOC = ocSchulz["O.C."].to_list() #lista de todas as OCs da coluna O.C.
listaQtd = ocSchulz["Qtd Ordem"].to_list() #lista de todas as quantidades de itens da coluna Qtd Ordem
'''

#LANÇANDO O VENDEDOR
try:
    posBoxSelecinarVendedor = pag.locateAllOnScreen(r"imagensOCR\boxSelecionarVendedor.png", confidence = 0.8)
except Exception as erro:
    alertaException("❌ Não foi possível localizar o Box do Vendedor!", erro)
    posBoxSelecinarVendedor = None

if(posBoxSelecinarVendedor):
    try:
        pag.click(posBoxSelecinarVendedor)
        pag.write("Automático")
        time.sleep(1.5)
        pag.press("enter")
        print("🤖 Vendedor 'Automático' selecionado!")
    except Exception as erro:
        alertaException("❌ Não foi possível Selecionar Vendedor: 'Automático':", erro)

#LANÇANDO PRODUTOS da OC
contador = 0
for i in listaItemFaturar:
    contador += 1
    pag.hotkey("Shift" , "F2")
    time.sleep(2)

    try:
        posBoxSelecionarProduto = pag.locateOnScreen(r"imagensOCR\boxSelecionarProduto.png", confidence = 0.8)
    except Exception as erro:
        alertaException("❌ Não foi possível localizar o Box de Produto!", erro)
        posBoxSelecionarProduto = None
        break





#Shift + F2 é o atalho para adicionar item no Pedido! Não necessita do OCR para achar o botão
#Somente depois de informar a Quantidade da OC o código pode usar o TAB para inserir o valor do contrato
#Só irá faturar mais produtos se houver mais de 1 produto na MESMA OC, se a OC for diferente é necessário outra Nota!

