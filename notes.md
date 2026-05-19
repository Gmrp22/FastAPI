# FastAPI Notes

## Parameter Validation

FastAPI valida los params automáticamente usando los type hints de Python.

```python
@app.get("/books/{id}")
def get_book(id: int):  # FastAPI convierte y valida antes de entrar a la función
```

- `/books/2` → llega como `int 2`, todo bien
- `/books/2s` → FastAPI rechaza con `422 Unprocessable Entity` antes de que tu código corra
- No necesitas `if type(id) != int` ni nada manual — el hint hace el trabajo

El 422 es el estándar HTTP para "datos con formato incorrecto". No hay que cambiarlo a menos que el cliente espere 400.

---

## Path Params vs Query Params

**Path param** → identifica *cuál* recurso quieres. Es parte de la identidad del recurso.

```
/books/2         → el libro con id 2
/users/juan      → el usuario juan
```

**Query param** → modifica *cómo* traes ese recurso. Es opcional y no cambia qué recurso es.

```
/books?genre=fiction         → filtra
/books?sort=year&order=asc   → ordena
/books?page=2&limit=10       → pagina
```

En FastAPI un query param es cualquier param de la función que no esté en la ruta:

```python
@app.get("/books/{book_author}")
def get_books(book_author: str, category: str = "all"):
    #          ↑ path param         ↑ query param (opcional, default "all")
```

Se llama así: `/books/Jane Austen?category=Romance`

---

## List Comprehension

Forma de Python de filtrar/transformar listas en una línea. Equivalente al `.filter()` de JS.

```python
# JS
books_db.filter(book => book.author === book_author)

# Python
[book for book in books_db if book.get("author") == book_author]
```

Estructura: `[lo_que_guardas   for variable in lista   if condicion]`

```python
# Guardar el objeto completo
[book for book in books_db if book.get("author") == "Jane Austen"]

# Guardar solo un campo
[book.get("title") for book in books_db if book.get("author") == "Jane Austen"]
# → ["Pride and Prejudice"]
```

Es equivalente a:

```python
result = []
for book in books_db:
    if book.get("author") == "Jane Austen":
        result.append(book)
```
