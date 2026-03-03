# Clase: Docker Compose

## Estructura del proyecto

```
.
├── docker-compose.yml   # Orquestación de servicios
├── react-app/           # Frontend React (Vite + TypeScript, servido con nginx)
└── py-app/              # Backend FastAPI (Python)
```

---

# Pushear a un registro: 
react-app
```bash
docker build -t react-app:1.0-dev
docker tag react-app:1.0-dev <registry>/<namespace>/<repository>:front-1.0-dev
docker push <registry>/<namespace>/<repository>:front-1.0-dev
```

py-app
```bash
docker build -f ./Dockerfile -t py-app:1.0-dev .
docker tag py-app:1.0-dev <registry>/<namespace>/<repository>:back-1.0-dev # (tag)
docker push <registry>/<namespace>/<repository>:back-1.0-dev
```
---

## Errores comunes

- **Usar `latest` como tag de imagen**
  `latest` no garantiza reproducibilidad. Si alguien hace `docker pull` en otro momento puede obtener una versión diferente. Siempre usar tags semánticos (`1.0.0`, `2.3.1`).

- **No usar `.dockerignore`**
  Sin él, el contexto de build incluye `node_modules/`, `.venv/`, `.git/` y otros directorios pesados, haciendo los builds lentos e impredecibles.

- **Copiar secretos en la imagen**
  Archivos `.env` con credenciales que se copian con `COPY . .` quedan embebidos en la imagen y son visibles con `docker history`. Usar variables de entorno en `docker-compose.yml` o secrets de Docker.

- **No fijar versiones**
  `pip install flask` o `npm install react` sin versión puede romper el build en cualquier momento. Siempre pinear: `flask==3.1.0`, `"react": "^19.0.0"`.

- **(Especifico de react-app) No commitear `package-lock.json`**
  El Dockerfile usa `npm ci`, que requiere un `package-lock.json` existente. Sin él el build falla. Antes del primer `docker compose up --build` hay que correr `npm install` dentro de `react-app/` para generar el lockfile, y commitearlo. `npm ci` es intencionalmente más estricto que `npm install`: instala exactamente lo que dice el lockfile, sin resolver versiones, lo que hace los builds reproducibles.

- **No respetar el orden de las capas en el Dockerfile**
  Copiar todo el código antes de instalar dependencias invalida la caché de `pip install` / `npm ci` en cada cambio de código. Siempre copiar primero los archivos de dependencias, instalar, y después copiar el resto.

---

## Comandos útiles

```bash
# Levantar todo (construye imágenes si es necesario)
docker compose up --build

# Levantar en background
docker compose up --build -d

# Ver logs de un servicio específico
docker compose logs -f py-app

# Bajar servicios (los volúmenes con nombre se conservan)
docker compose down

# Bajar servicios y eliminar volúmenes
docker compose down -v

# Ver imágenes locales
docker images
```
