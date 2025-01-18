import requests
from bs4 import BeautifulSoup
print("Bem-vindo ao Pesquisador!")
print("O que você deseja fazer?")
while True:
    decisao = input("digite 1 para pesquisar 2 para ver a previsão do tempo e 3 para sair : ")
    if decisao == "1":
        print("escreva sobre o que você quer saber. evite formar frases.")
        # Entrada de pesquisa
        pesquisa = input("Digite sua pesquisa: ")
        pesquisa = pesquisa.replace("o que é uma ", "")
        pesquisa = pesquisa.replace("o que é um ", "")
        pesquisa = pesquisa.replace("o que é o ", "")
        pesquisa = pesquisa.replace("o que é a ", "")
        pesquisa = pesquisa.replace("o que é ", "")
        pesquisa = pesquisa.replace("o que são os", "")
        pesquisa = pesquisa.replace("o que são as", "")
        pesquisa = pesquisa.replace("o que são ", "")
        pesquisa = pesquisa.replace("quem é o ", "")
        pesquisa = pesquisa.replace("quem é a ", "")
        pesquisa = pesquisa.replace("quem é ", "")
        pesquisa = pesquisa.replace("quem são os ", "")
        pesquisa = pesquisa.replace("quem são as ", "")
        pesquisa = pesquisa.replace("quem são ", "")
        pesquisa = pesquisa.replace("quem foi os ", "")
        pesquisa = pesquisa.replace("quem foi as ", "")
        pesquisa = pesquisa.replace("quem foi ", "")
        pesquisa = pesquisa.replace("quem foram os ", "")
        pesquisa = pesquisa.replace("quem foram as ", "")
        pesquisa = pesquisa.replace("quem foram ", "")
        pesquisa = pesquisa.replace("quem foi o ", "")
        pesquisa = pesquisa.replace("quem foi a ", "")
        pesquisa = pesquisa.replace("o que foi o ", "")
        pesquisa = pesquisa.replace("o que foi a ", "")
        pesquisa = pesquisa.replace("o que foi ", "")

        # Faz a requisição
        ir = requests.get("https://pt.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles="+pesquisa+"&exintro=true&explaintext=true")

        if ir.status_code == 200:
            data = ir.json()

            # Verifica se a página foi encontrada
            pages = data["query"]["pages"]
            page = list(pages.values())[0]

            if "missing" in page or not page.get("extract"):  # Verifica se a página não existe ou não tem 'extract'
                pesquisa = pesquisa.replace(" ", "_")
                print(pesquisa.title())
                # Faz a requisição HTTP
                ir = requests.get("https://pt.wikipedia.org/wiki/" + pesquisa.title())
                pesquisouja = ir.text
                posinicial = pesquisouja.find("<p><b>", 0)  # Localiza a abertura "<"     
                posfinal = pesquisouja.find(".", posinicial)  # Localiza o fechamento ">"
                pesquisouja = pesquisouja[posinicial:posfinal + 1]  # Inclui o ">"
                if "<b>A Wikipédia não possui um artigo com este nome exato.</b>" in ir.text or ir.text == "":
                    print("Página não encontrada")
                else:
                    html = []
                    start = 0

                    # Coleta os trechos entre "<" e ">" do HTML
                    while "<" in pesquisouja and ">" in pesquisouja:
                        posinicial = pesquisouja.find("<")
                        posfinal = pesquisouja.find(">", posinicial)
                        if posfinal == -1:
                            break  # Garante que não ocorra erro se não houver ">"
                        pesquisouja = pesquisouja[:posinicial] + pesquisouja[posfinal + 1:]
                    print(pesquisouja)
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
    elif decisao == "2":
        graus = requests.get("https://weather.com")
        if graus.status_code == 200:
            posinicial = graus.text.find("<span data-testid=\"TemperatureValue\" class=\"CurrentConditions--tempValue--zUBSz\" dir=\"ltr\">", 0)
            # Identificar posicao final do link
            posfinal = graus.text.find("<span class=\"CurrentConditions--degreeSymbol--tzLy9\">°</span><span></span></span>", posinicial)
            # Extrai texto das posições identificadas
            substring = graus.text[posinicial:posfinal]
            substring = substring.replace("<span data-testid=\"TemperatureValue\" class=\"CurrentConditions--tempValue--zUBSz\" dir=\"ltr\">", "")
            print("na sua cidade faz " + substring + " graus")
        else:
            print("Erro ao acessar a previsão do tempo.")
    elif decisao == "3":
        print("Até mais!")
        break
