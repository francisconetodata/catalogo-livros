# main.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# --- Modelos Pydantic ---
# Modelo base para os dados do livro (sem ID, usado para criação)
class LivroBase(BaseModel):
    titulo: str = Field(..., description="Título do livro") # ... significa obrigatório
    autor: str = Field(..., description="Autor do livro")
    ano_publicacao: Optional[int] = Field(None, description="Ano de publicação do livro")
    genero: Optional[str] = Field(None, description="Gênero do livro")

# Modelo para criação de livro (herda de LivroBase)
class LivroCreate(LivroBase):
    pass # Sem campos adicionais necessários para criação

# Modelo para atualização de livro (todos os campos são opcionais)
class LivroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    ano_publicacao: Optional[int] = None
    genero: Optional[str] = None

# Modelo completo do livro, incluindo ID (usado para respostas)
class Livro(LivroBase):
    id: int = Field(..., description="Identificador único do livro")

    # Configuração para permitir que o Pydantic funcione bem com objetos ORM/dicionários
    # class Config:
    #     orm_mode = True # Descomentar se usar ORM, mas não necessário para dicionários

# --- Armazenamento em Memória ---
# Usaremos um dicionário para simular um banco de dados
# A chave será o ID do livro, e o valor será o objeto Livro
db_livros: Dict[int, Livro] = {}
ultimo_id_livro: int = 0 # Contador simples para gerar IDs únicos

# --- Instância do FastAPI ---
app = FastAPI(
    title="API Livraria Coruja",
    description="API para gerenciar o catálogo de livros da Livraria Coruja.",
    version="1.0.0"
)

# --- Endpoints ---

@app.post(
    "/livros",
    response_model=Livro,
    status_code=status.HTTP_201_CREATED,
    summary="Adiciona um novo livro ao catálogo",
    tags=["Livros"] # Agrupa endpoints na documentação interativa
)
def criar_livro(livro: LivroCreate):
    """
    Cria um novo livro com base nos dados fornecidos:

    - **titulo**: Título do livro (obrigatório)
    - **autor**: Autor do livro (obrigatório)
    - **ano_publicacao**: Ano de publicação (opcional)
    - **genero**: Gênero do livro (opcional)

    Retorna o livro criado com seu ID único.
    """
    global ultimo_id_livro
    ultimo_id_livro += 1
    novo_livro = Livro(
        id=ultimo_id_livro,
        **livro.model_dump() # Desempacota os dados de LivroCreate
    )
    db_livros[novo_livro.id] = novo_livro
    return novo_livro

@app.get(
    "/livros",
    response_model=List[Livro],
    summary="Lista todos os livros do catálogo com paginação",
    tags=["Livros"]
)
def listar_livros(skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de livros do catálogo.

    - **skip**: Número de livros a pular (para paginação).
    - **limit**: Número máximo de livros a retornar.
    """
    # Converte os valores do dicionário (objetos Livro) em uma lista
    livros_lista = list(db_livros.values())

    # Validação básica para skip e limit
    if skip < 0:
        skip = 0
    if limit <= 0:
        limit = 10 # Ou algum outro default razoável

    # Aplica paginação
    return livros_lista[skip : skip + limit]

@app.get(
    "/livros/{livro_id}",
    response_model=Livro,
    summary="Obtém detalhes de um livro específico",
    tags=["Livros"]
)
def obter_livro(livro_id: int):
    """
    Retorna os detalhes de um livro específico pelo seu ID.

    - **livro_id**: ID do livro a ser recuperado.

    Levanta um erro 404 se o livro não for encontrado.
    """
    livro = db_livros.get(livro_id)
    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com id {livro_id} não encontrado"
        )
    return livro

@app.put(
    "/livros/{livro_id}",
    response_model=Livro,
    summary="Atualiza um livro existente",
    tags=["Livros"]
)
def atualizar_livro(livro_id: int, livro_update: LivroUpdate):
    """
    Atualiza as informações de um livro existente identificado pelo ID.
    Apenas os campos fornecidos no corpo da requisição serão atualizados.

    - **livro_id**: ID do livro a ser atualizado.
    - **livro_update**: Objeto contendo os campos a serem atualizados (titulo, autor, ano_publicacao, genero).

    Levanta um erro 404 se o livro não for encontrado.
    """
    livro_existente = db_livros.get(livro_id)
    if livro_existente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com id {livro_id} não encontrado"
        )

    # Obtém os dados de atualização, excluindo campos não definidos (None)
    update_data = livro_update.model_dump(exclude_unset=True)

    # Atualiza os campos do livro existente
    # Note: Isso funciona porque estamos trabalhando com objetos Pydantic em memória.
    # Se fosse um ORM, usaríamos métodos específicos do ORM.
    for key, value in update_data.items():
        setattr(livro_existente, key, value)

    # Atualiza o livro no "banco de dados" (dicionário)
    db_livros[livro_id] = livro_existente # Redundante se setattr modificou o objeto original, mas seguro

    return livro_existente

@app.delete(
    "/livros/{livro_id}",
    status_code=status.HTTP_200_OK, # Ou pode ser 204 No Content se não retornar corpo
    summary="Remove um livro do catálogo",
    tags=["Livros"]
)
def deletar_livro(livro_id: int):
    """
    Remove um livro do catálogo pelo seu ID.

    - **livro_id**: ID do livro a ser removido.

    Levanta um erro 404 se o livro não for encontrado.
    Retorna uma mensagem de confirmação.
    """
    if livro_id not in db_livros:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com id {livro_id} não encontrado"
        )

    del db_livros[livro_id]
    # Alternativa: usar status_code=status.HTTP_204_NO_CONTENT e retornar None
    return {"mensagem": f"Livro com id {livro_id} removido com sucesso"}


# --- Rota Raiz (Opcional) ---
@app.get("/", summary="Rota raiz da API", include_in_schema=False) # Oculta da documentação Swagger/ReDoc
def read_root():
    return {"Bem-vindo": "API da Livraria Coruja"}

# Instruções para rodar (não faz parte do código executável, mas é útil)
# Para rodar a API, salve este código como main.py e execute no terminal:
# uvicorn main:app --reload