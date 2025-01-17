import requests
from bs4 import BeautifulSoup
print("Bem-vindo ao Pesquisador!")
decisao = input("digite 1 para pesquisar e outra coisa para ver a previsão do tempo : ")
if decisao == "1":
    print("escreva sobre o que você quer saber. evite formar frases.")
# Entrada de pesquisa
    pesquisa = input("Digite sua pesquisa: ")
    pesquisa = pesquisa.replace("o que é uma ", "")
    pesquisa = pesquisa.replace("o que é um ", "")
    pesquisa = pesquisa.replace("o que é o ", "")
    pesquisa = pesquisa.replace("o que é a ", "")
    pesquisa = pesquisa.replace("o que é ", "")
# Faz a requisição
    ir = requests.get("https://pt.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles="+pesquisa+"&exintro=true&explaintext=true")

    if ir.status_code == 200:
        data = ir.json()

    # Verifica se a página foi encontrada
        pages = data["query"]["pages"]
        page = list(pages.values())[0]

        if "missing" in page or page == "" or page == " ":  # Verifica se a página não existe
            ir = requests.get("https://blog.eurekka.me/"+pesquisa)
            soup = BeautifulSoup(ir.text, 'html.parser')
            texto = soup.find_all('p')
            if ir.text.find("A página que você solicitou não foi encontrada") >-1 or ir.text == "":
                print("Página não encontrada")
            else:
                print(texto)
        else:
        # Exibe o primeiro parágrafo (extract)
            texto = page["extract"]
            print(texto)

    else:  # Se a Wikipédia não funcionar, busca no blog
        ir = requests.get("https://blog.eurekka.me/"+pesquisa)

        if ir.status_code == 200:
            soup = BeautifulSoup(ir.text, "html.parser")
            texto = soup.find_all("p")

            if "A página que você solicitou não foi encontrada" in ir.text:
                print("Página não encontrada no blog!")
            else:
                print("Resultados encontrados no blog:")
                for paragrafo in texto[:3]:  # Exibe os 3 primeiros parágrafos
                    print(paragrafo.get_text())
        else:
            print("Erro ao acessar a página! tente resumir a pesquisa.") 
else:
    graus = requests.get("https://weather.com")
    if graus.status_code == 200:
        posinicial = graus.text.find("<span data-testid=\"TemperatureValue\" class=\"CurrentConditions--tempValue--zUBSz\" dir=\"ltr\">",0)
# Identificar posicao final do link
        posfinal = graus.text.find("<span class=\"CurrentConditions--degreeSymbol--tzLy9\">°</span><span></span></span>",posinicial)
# Extrai texto das posições identificadas
        substring = graus.text[posinicial:posfinal]
        substring = substring.replace("<span data-testid=\"TemperatureValue\" class=\"CurrentConditions--tempValue--zUBSz\" dir=\"ltr\">","")
        print("na sua cidade faz " + substring + " graus")
    else:
        print("Erro ao acessar a previsão do tempo.")
