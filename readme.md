# Desafio FastAPI: API de Catálogo de Livros Simples

### Contexto Fictício:

Você foi contratado por uma pequena livraria independente, a "Livraria Coruja", que deseja começar a digitalizar seu inventário. Como primeiro passo, eles precisam de uma API simples para gerenciar as informações básicas dos livros em seu catálogo. Eles não precisam (ainda) de gerenciamento de estoque ou vendas, apenas das informações descritivas dos livros. A API deve permitir adicionar novos livros, visualizar todos os livros, ver detalhes de um livro específico, atualizar informações de um livro e remover um livro do catálogo.

### Requisitos Técnicos:

Tecnologia: Use Python e FastAPI.

#### Modelo de Dados (Livro): Cada livro deve ter os seguintes campos:

id: Um identificador único para cada livro (inteiro, gerado automaticamente pela API).
titulo: Título do livro (string, obrigatório).
autor: Nome do autor (string, obrigatório).
ano_publicacao: Ano em que o livro foi publicado (inteiro, opcional).
genero: Gênero do livro (string, opcional).
Armazenamento: Para este desafio, use um armazenamento de dados em memória (um dicionário ou lista Python será suficiente). Não é necessário usar um banco de dados real.

##### Endpoints (Rotas): A API deve expor os seguintes endpoints:

POST /livros: Adiciona um novo livro ao catálogo. Deve receber os dados do livro (título, autor, ano, gênero) no corpo da requisição e retornar o livro recém-criado com seu id. Status code: 201 Created.

GET /livros: Retorna uma lista de todos os livros no catálogo. Deve suportar parâmetros de consulta (query parameters) para paginação básica: skip (pular N itens, default 0) e limit (retornar no máximo N itens, default 10). Status code: 200 OK.

GET /livros/{livro_id}: Retorna os detalhes de um livro específico, identificado pelo seu id. Se o livro não for encontrado, retornar um erro 404 Not Found. Status code: 200 OK.

PUT /livros/{livro_id}: Atualiza as informações de um livro existente. Deve receber os novos dados no corpo da requisição. Se o livro não for encontrado, retornar 404 Not Found. Retorna o livro atualizado. Status code: 200 OK.

DELETE /livros/{livro_id}: Remove um livro do catálogo pelo seu id. Se o livro não for encontrado, retornar 404 Not Found. Retornar uma mensagem de sucesso. Status code: 200 OK.

Validação: Use modelos Pydantic para definir a estrutura dos dados de entrada (corpo da requisição) e saída (resposta). Os campos obrigatórios (titulo, autor) devem ser validados.

Tratamento de Erros: Implemente o tratamento de erro para livros não encontrados (404 Not Found).

### Entregável:

Um único arquivo Python (main.py, por exemplo) contendo a implementação completa da API FastAPI.