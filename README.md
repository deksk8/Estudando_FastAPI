# Estudando FastAPI

## Iniciando os trabalho realizando o download:
Para dar start no estudo desse framework, primeiro vamos realizar o download e a instalação. Para tal, usar o comando:

	pip install fastapi uvicorn
	
-   **FastAPI**: o framework em si.
-   **uvicorn**: um servidor rápido e leve que executa aplicações ASGI, necessário para rodar a aplicação FastAPI.

Depois de instalado, vamos ao nossa primeira aplicação. Crie um arquivo `Python`, por exemplo, `main.py` e execute o seguinte código:

    from fastapi import FastAPI

	app = FastAPI()

	@app.get("/")
	def read_root():
	    return {"mensagem": "Bem-vindo à minha primeira aplicação FastAPI!"}

Depois de digitado o código. ***(Sugestão: digite mesmo)*** . Execute o servidor `uvicorn`:

    unicorn main:app --reload
    
Se tudo tiver funcionando bem, você deve ver alguma coisa desse tipo no seu terminal:

<a href="https://ibb.co/ZLNC0Hq"><img src="https://i.ibb.co/HFXQjN5/image.png" alt="image" border="0"></a>

E acesso o link: `127.0.0.1:8000`, você deverá ver algo parecido com isso no navegador:

<a href="https://imgbb.com/"><img src="https://i.ibb.co/xJL5hXs/image.png" alt="image" border="0"></a>

-   O parâmetro `--reload` faz com que o servidor seja recarregado automaticamente sempre que você salvar alterações no código.
-   A aplicação estará disponível, por padrão, em `http://127.0.0.1:8000`.

### 3.1 Verificando a Documentação Automática

-   Visite http://127.0.0.1:8000/docs para ver a interface **Swagger**.
-   Visite http://127.0.0.1:8000/redoc para ver a interface **ReDoc**.

## Código teste de algumas funções:
Para avançar no estudo do `FastAPI`, desenvolvi o seguinte código:

Imports interessantes:
---

	from fastapi import FastAPI#, HTTPException
	from pydantic import BaseModel
	import requests

Com `HTTPException`  é possível tratar exceções HTTP, deixando o código mais sofisticado. Já com o `requests` é possível realizar requisições HTTP. Utilizar mas ele é **altamente recomendado** e a prática padrão ao construir APIs com validação de dados. O **Pydantic** é a biblioteca por trás do FastAPI que fornece a funcionalidade de validação de dados de maneira eficiente, automática e estruturada. Será mostrado adiante, um exemplo utilizando o verbo `POST` com e sem o `BaseModel`.

Definindo o primeiros endpoints
---
	@app.get("/")

	def  home():

	return{  "mensagem":  "Bem-vido a minha primeira aplicação FASTAPI!"  }

	  

	@app.get("/rafael")

	def  rafael():

	return{  "mensagem":  "Receba Rafael"  }

Em ambos endpoinst `/` e `/rafael`, o retorno dessa request `/GET` são dicionários. Um tipo de retorno simples

Passando parâmetros
-
Os próximos dois endpoints, são recebem parâmetros de duas formas: 

 **1. Parâmetros no caminho (path parameter)**
 **2. Parâmetros na query (query parameter)**

O código abaixo mostra um exemplo de um `path parameter`:

	#Passando parâmetros direto na url: minhagatinha/10

	@app.get("/minhagatinha/{vezes}")

	def  minha_gatinha(vezes:  int):

	return{  "mensagem":  f"Te amo, minha gatinha! {vezes} vezes"  }

E a segue um exemplo de um `query parameter`	  

	#Passando parâmetros para url via query

	@app.get("/buscacep")

	def  buscar_cep(cep:  str  =  None):

O restante do código são tratamentos do parametros de entrada e a requisição

	#Verificar se o CEP foi fornecido
	
	if  not cep:

	#raise HTTPException(status_code=400, detail="O parâmetro 'cep' é obrigatório.")

	return  {  "O parâmetro cep é obrigatório"  }

	#Montar a URL para a API ViaCEP

	url =  f"https://viacep.com.br/ws/{cep}/json/"

	  

	req = requests.get( url )

	  

	if req.status_code !=  200:

	return  {  "mensagem":  f"Valor do cep inválido. request erro {req.status_code}"  }

	  

	#Fazer a requisição para a API ViaCEP

	#Nesse exemplo o GPT utilizou um função mais sofisticada. Fazendo o tratamento de uma exceção.

	#mas não era essa a minha finalidade, então estou fazendo o tratamento manualmente.

	#

	#try:

	#req = requests.get(url)

	#req.raise_for_status() # Lança exceção se o status for de erro (4xx ou 5xx)

	#except requests.exceptions.RequestException as e:

	#raise HTTPException(status_code=500, detail=f"Erro ao acessar a API ViaCEP: {e}")

	#

	##Retornar os dados como JSON

	#dados = req.json()

	#if "erro" in dados:

	#raise HTTPException(status_code=404, detail="CEP não encontrado.")

	  

	return req.json()

Rotas com o verbo `POST`
-
No código foi inserido duas rotas, uma utilizando o `BaseModel` e outra sem utilizá-lo. Segue os códigos:

## Exemplo Sem BaseModel

    # Exemplo sem o uso do Basemodel:
	#O dados são simplimente enviados e recebido, sem tratamentos

	@app.post("/dados")
	def  receber_dados(dados:  dict):
	return  {"recebido": dados}

**Enviando:**

<a href="https://imgbb.com/"><img src="https://i.ibb.co/PtrzFNV/image.png" alt="image" border="0"></a>

**Resposta:**

<a href="https://imgbb.com/"><img src="https://i.ibb.co/L0Pz8vH/image.png" alt="image" border="0"></a>

## Exemplo Com BaseModel

    # Exemplo com o BaseModel

	#Nesse exemplo, o BaseModel amarra a estrutura do dado enviado,
	#caso no momento da requisição, faltar algum campo ele enviar o código de erro: 402

	class  Pessoa(BaseModel):
		nome:str
		idade:int
		trabalhando:  bool
		renda:  float
	@app.post("/pessoa")
	def  criar_pessoa(pessoa: Pessoa):
		return  {  "mensagem":  f"Pessoa {pessoa.nome} com idade {pessoa.idade} está trabalhando {pessoa.trabalhando} "  }

**Enviando request:**

<a href="https://imgbb.com/"><img src="https://i.ibb.co/Fx3zHNL/image.png" alt="image" border="0"></a>

**Resposta:**
<a href="https://imgbb.com/"><img src="https://i.ibb.co/PMFGZ0K/image.png" alt="image" border="0"></a>

## Testando formato do BaseModel

**Enviando request:**

<a href="https://imgbb.com/"><img src="https://i.ibb.co/BfgvWjc/image.png" alt="image" border="0"></a>

**Resposta:**

<a href="https://imgbb.com/"><img src="https://i.ibb.co/yVjj7Fk/image.png" alt="image" border="0"></a>

## Conclusões iniciais:

Após esses teste, posso concluir facilmente que o FastAPI é uma ferramenta excelente para desenvolvimento de backend. Seja pela facilidade de desenvolvimento, seja pela sua praticidade na geração da documentação automática.
Os estudos continuarão.... Nos vemos em breve....
