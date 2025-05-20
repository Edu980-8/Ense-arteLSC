## 🐳 **Docker Compose**

### ✅ 1. Levantar solo el servicio `db`:

```bash
docker compose up db
```

> Si necesitas que corra en segundo plano (detached mode):

```bash
docker compose up -d db
```

---

### 🧹 2. Parar todos los servicios y borrar volúmenes:

```bash
docker compose down -v
```

> Este comando detiene todos los contenedores y elimina los volúmenes asociados (por ejemplo, los datos de PostgreSQL).

---

## 🐍 **Alembic con `uv`**

### 📋 3. Revisiones (generar archivo de migración):

```bash
uv run alembic revision --autogenerate -m "mensaje_descriptivo"
```

> Asegúrate de que tu archivo `alembic.ini` y `env.py` estén bien configurados para apuntar a tu modelo de datos y URL de base de datos.

---

### ⚙️ 4. Aplicar migraciones (upgrade):

```bash
uv run alembic upgrade head
```

> Esto aplica todas las migraciones pendientes hasta la más reciente (`head`).

---

### 🧪 Otras útiles:

* Ver historial de migraciones:

  ```bash
  uv run alembic history
  ```

* Downgrade (por ejemplo, una versión atrás):

  ```bash
  uv run alembic downgrade -1
  ```
