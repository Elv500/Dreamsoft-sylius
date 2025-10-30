# DIPLOMADO INGENIERÍA DE CALIDAD DE SOFTWARE COMERCIAL (3ra Edición)
#### CARRERA DE INGENIERÍA INFORMÁTICA
### PROYECTO FINAL - FRAMEWORK DE PRUEBAS AUTOMATIZADAS REST API DE SYLIUS

---

# Grupo: DreamSoft  
## **Autor:** Alvarez Cayo Elvis [![GitHub](https://img.shields.io/badge/GitHub-Elv500-blue?logo=github)](https://github.com/Elv500)

---
## Requisitos Previos
- Python 3.13.x o superior
- pip (incluido con Python)
- Git (para clonar el repositorio)
- Allure CLI (opcional, para reportes visuales)
- IDE VSCode o PyCharm

# Instalación y Configuración
1. Clonar el repositorio
```bash
git clone https://github.com/Elv500/Dreamsoft-sylius.git
cd Dreamsoft-sylius
```
2. Crear y activar un entorno virtual
- En **Windows**:

  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

- En **macOS/Linux**:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
3. Instalar dependencias
```bash
pip install -r requirements.txt
```
4. Configurar variables de entorno

    Duplica o cambia el nombre del archivo .env.example a **.env**
    ```bash
    BASE_URL=ingresar_ruta_api
    ADMIN_EMAIL=ingresar_email_admin
    ADMIN_PASSWORD=ingresar_contrasena_admin
    ```
> Con estas configuraciones, ya se tiene listo para la ejecución de pruebas.

# Ejecución de Pruebas
Para la ejecucion de pruebas, se tiene distintas maneras.
1. Ejecución completa rápida
    ```bash
    pytest
    ```
2. Ejecución completa detallada
    ```bash
    pytest -v
    ```

# Generación y visualización de reportes
Para la generación de reportes, se tiene las siguientes dos opciones que ya vienen integratos en `requeriments.txt`:
## Opción 1: Pytest HTML
Para generar reporte con pytest html sigue los siguientes pasos:
1. Generar reporte
    ```bash
    pytest --html=reports/reports_general.html 
    ```
2. Visualizar reporte

    Abrir en su navegador preferido el archivo `reports_general.html`

## Opción 2: Allure Reports
Para generar reporte con allure sigue los siguientes pasos:
1. Generar reporte
    ```bash
    pytest --alluredir=reports/allure-results 
    ```
Se debe tener instalado `Allure CLI` previamente para poder generar un reporte HTML o levantarlo un servidor local y ver el reporte directamente:
> Puede revisar el siguiente enlace para Allure CLI: https://github.com/allure-framework/allure2/releases/tag/2.34.1
2. Visualizar reporte
    ```bash
    allure serve reports/allure-results
    ```

3. Opcion extra Allure HTML

    Tambien se puede generar el `Reporte Allure HTML`
    ```bash
    allure generate reports/allure-results --clean -o reports/allure-report-html
    allure open reports/allure-report-html 
    ```
    > Se agrega el `--clean -o` para que no se acumule todos los reportes y se actualice a la última versión.

    Esto abrirá un navegador con el reporte visual de los resultados.
