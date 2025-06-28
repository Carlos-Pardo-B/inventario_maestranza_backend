# Inventario Maestranza - Backend Django

## 🛠️ Configuración inicial

### Requisitos previos
- Python 3.8+
- Git
- pip

### 1. Clonar el repositorio
git clone https://github.com/Carlos-Pardo-B/inventario_maestranza_backend.git

cd inventario_maestranza_backend

### 2. Crear entorno virtual e activarlo
python -m venv venv

venv\Scripts\activate

### 3. Instalar dependencias
pip install -r requirements.txt

### 4. Crear base de datos
python manage.py migrate

### 5. Cargar datos
python manage.py loaddata db_backup.json

### 6. Arrancar Backend
python manage.py runserver