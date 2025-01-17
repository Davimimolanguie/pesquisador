import requests
from bs4 import BeautifulSoup

# Entrada de pesquisa
pesquisa = input("Digite sua pesquisa: ")

# Faz a requisição
ir = requests.get("https://pt.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles="+pesquisa+"&exintro=true&explaintext=true")

if ir.status_code == 200:
    data = ir.json()

    # Verifica se a página foi encontrada
    pages = data["query"]["pages"]
    page = list(pages.values())[0]

    if "missing" in page:  # Verifica se a página não existe
        ir = requests.get("https://blog.eurekka.me/"+pesquisa)
        soup = BeautifulSoup(ir.text, 'html.parser')
        texto = soup.find_all('p')
        if ir.text.find("A página que você solicitou não foi encontrada") >-1:
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
        print("Erro ao acessar o blog.")
