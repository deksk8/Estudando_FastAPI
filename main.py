from fastapi import FastAPI#, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

@app.get("/")
def home():
    return{ "mensagem": "Bem-vido a minha primeira aplicação FASTAPI!" }

@app.get("/rafael")
def rafael():
    return{ "mensagem": "Receba Rafael" }

#   Passando parâmetros direto na url: minhagatinha/10
@app.get("/minhagatinha/{vezes}")
def minha_gatinha(vezes: int):
    return{ "mensagem": f"Te amo, minha gatinha! {vezes} vezes" }

#   Passando parâmetros para url via query
@app.get("/buscacep")
def buscar_cep(cep: str = None):
    # Verificar se o CEP foi fornecido
    print(f"O valor do: {cep}")

    if not cep:
#        raise HTTPException(status_code=400, detail="O parâmetro 'cep' é obrigatório.")
        return { "O parâmetro cep é obrigatório" }  
    # Montar a URL para a API ViaCEP
    url = f"https://viacep.com.br/ws/{cep}/json/"

    req = requests.get( url )

    if req.status_code != 200:
        return { "mensagem": f"Valor do cep inválido. request erro {req.status_code}" }

    # Fazer a requisição para a API ViaCEP
#   Nesse exemplo o GPT utilizou um função mais sofisticada. Fazendo o tratamento de uma exceção.
#   mas não era essa a minha finalidade, então estou fazendo o tratamento manualmente.
#  
#    try:
#        req = requests.get(url)
#        req.raise_for_status()  # Lança exceção se o status for de erro (4xx ou 5xx)
#    except requests.exceptions.RequestException as e:
#        raise HTTPException(status_code=500, detail=f"Erro ao acessar a API ViaCEP: {e}")
#    
#    # Retornar os dados como JSON
#    dados = req.json()
#    if "erro" in dados:
#        raise HTTPException(status_code=404, detail="CEP não encontrado.")

    return req.json()

#   Exemplo sem o uso do Basemodel:
#   O dados são simplimente enviados e recebido, sem tratamentos
@app.post("/dados")
def receber_dados(dados: dict):
    return {"recebido": dados}

#   Exemplo com o BaseModel
#   Nesse exemplo, o BaseModel amarra a estrutura do dado enviado,
#   caso no momento da requisição, faltar algum campo ele enviar o código de erro: 402
class Pessoa(BaseModel):
    nome:str
    idade:int
    trabalhando: bool
    renda: float
@app.post("/pessoa")
def criar_pessoa(pessoa: Pessoa):
    return { "mensagem": f"Pessoa {pessoa.nome} com idade {pessoa.idade} está trabalhando {pessoa.trabalhando} " }