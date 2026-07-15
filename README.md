# API Fast Test (FastAPI + PostgreSQL + GraphQL + REST)

Este proyecto es una API construida con **FastAPI** que integra **PostgreSQL** (mediante SQLAlchemy y asyncpg) y ofrece endpoints tanto **REST** como **GraphQL** (usando Strawberry).

---

## 🛠️ Requisitos Previos

Asegúrate de tener instalado en tu sistema:
- **Docker** y **Docker Compose**
- **Python 3.12** (opcional, solo para ejecución local fuera de Docker)

---

## 🐳 Opción 1: Levantar con Docker (Recomendado)

Docker es el método más sencillo ya que configura automáticamente la base de datos PostgreSQL y la aplicación FastAPI en contenedores interconectados.

### Pasos para iniciar:

1. **Configurar el entorno**:
   Asegúrate de tener un archivo `.env` en la raíz del proyecto. El archivo `.env` ya viene preconfigurado por defecto con las siguientes variables:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=mydatabase
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/mydatabase
   SECRET_KEY=4f0f7c66d53dbef4b1d68db5c8e84e92cbad9d0e4d1c30d7f1a4a96b76d9d124
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

2. **Construir y levantar los contenedores**:
   Ejecuta el siguiente comando en la terminal desde la raíz del proyecto:
   ```bash
   docker compose up --build
   ```
   *Nota: Agrega `-d` al final si deseas ejecutar los contenedores en segundo plano (detached mode): `docker compose up --build -d`.*

3. **Verificación de tablas**:
   Al iniciar, el contenedor de FastAPI (`fastapi_app`) esperará a que PostgreSQL esté saludable (`healthy`) y luego creará automáticamente todas las tablas de la base de datos si no existen.

---

## 🐍 Opción 2: Ejecución Local (Fuera de Docker)

Si prefieres ejecutar la aplicación FastAPI directamente en tu máquina local:

### 1. Levantar solo la Base de Datos con Docker
Puedes usar Docker Compose para iniciar únicamente la base de datos PostgreSQL:
```bash
docker compose up db -d
```

### 2. Configurar el Entorno Virtual de Python (macOS / Linux)
Dado que los entornos de Python modernos protegen el sistema global de instalaciones accidentales (evitando errores de tipo `externally-managed-environment`), es necesario usar un entorno virtual (`venv`):

```bash
# 1. Crear el entorno virtual (si no lo has creado)
python3 -m venv venv

# 2. Activar el entorno virtual
source venv/bin/activate

# 3. Instalar las dependencias usando el flag -r (¡IMPORTANTE! Recuerda usar -r)
pip install -r requirements.txt
```

*Nota para Windows:*
Si estás en Windows, activa el entorno con:
`venv\Scripts\activate`

### 3. Iniciar el Servidor de Desarrollo
Una vez que las dependencias están instaladas y el entorno virtual está activo, corre el servidor con Uvicorn:
```bash
uvicorn app.main:app --reload
```

---

## 📍 Endpoints y Servicios Disponibles

Una vez que el proyecto esté corriendo (ya sea en Docker o Local):

- **REST API (Documentación Interactiva Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **REST API (Documentación Alternativa Redoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **GraphQL Playground (Consola Interactiva)**: [http://localhost:8000/graphql](http://localhost:8000/graphql)

---

## 🐳 Comandos Útiles de Docker

- **Detener los servicios**:
  ```bash
  docker compose down
  ```
- **Ver los logs en tiempo real**:
  ```bash
  docker compose logs -f
  ```
- **Detener y borrar los volúmenes de datos (reinicio de base de datos)**:
  ```bash
  docker compose down -v
  ```
# api-fastapi-graphql-modular
# api-fastapi-graphql-modular
# api-fastapi-graphql-modular
