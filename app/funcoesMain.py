import pyautogui as pag, pytesseract as pyt, os, time, pymsgbox, pandas, glob, PIL
import sqlPython, funcoesMain

def alertaPag(msg, pagFail):
    print(msg, pagFail)
    pymsgbox.alert(msg)

def alertaException(msg, erro):
    print(msg, erro)
    pymsgbox.alert(msg)

def alertaElse(msg):
    print(msg)
    pymsgbox.alert(msg)

def novaGuiaChrome():
    novaGuiaNaoEncontrada = False
    try:
        posNovaGuia = pag.locateOnScreen(r"imagensOCR\guiaNovaChrome.png", confidence = 0.8)
    except:
        print("🤖 Nova Guia não foi encontrada! Abrindo uma!")
        novaGuiaNaoEncontrada = True

    if(novaGuiaNaoEncontrada == True):
        try:
            posCriarNovaGuia = pag.locateOnScreen(r"imagensOCR\criarNovaGuia.png", confidence = 0.8)
            if(posCriarNovaGuia):
                pag.click(posCriarNovaGuia)
                print("✅ Nova guia criada com sucesso no browser do Chrome")
                novaGuiaNaoEncontrada = False
            else:
                alertaElse("❌ Não foi possível encontrar o botão de 'criar nova guia' no browser...")
        except Exception as error:
            alertaException("Erro encontrado:", error)
        
    if(novaGuiaNaoEncontrada == False):
        try:
            posNovaGuia = pag.locateOnScreen(r"imagensOCR\guiaNovaChrome.png", confidence = 0.8)
            pag.click(posNovaGuia)
            print("Encontrado Nova Guia para prosseguir com operação")
            time.sleep(0.3)

            posAbaPesquisa = pag.locateOnScreen(r"imagensOCR\pesquisaChrome.png", confidence = 0.9)
            if(posAbaPesquisa):
                pag.click(posAbaPesquisa)
                print("Pronto para inserir endereço HTTPS!")
            else:
                alertaElse("❌ Não foi possivel encontrar a Barra de Pesquisa do Browser")
        except Exception as erro:
            alertaException("ocorreu um erro:", erro)
        except pag.FailSafeException as pagFail:
            alertaPag("Código encerrado por PyAutoGui de forma segura!", pagFail)

def selecionarBox(img, texto):
    leitura = pyt.image_to_string(PIL.Image.open(img), lang = "eng")
    if(leitura == texto):
        print("deu boa")
    else:
        print("deu ruim")


def consultarEstoque():
    print("oi")

    