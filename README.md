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
    BASE_URL=https://v2.demo.sylius.com
    ADMIN_EMAIL=api@example.com
    ADMIN_PASSWORD=sylius-api
    ```
`Se adjunta las credenciales sin problema, porque son publicas en este caso.`
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

Con todo configurado, ya puedes correr las pruebas automatizadas de las siguientes maneras:

   > Si nota que su IDE ejecuta lento los tests, puede agregar el siguiente parametro a cualquier comando de ejecución:

   ```bash
   --cache-clear
   ```

### Ejecutar Regression

Para ejecutar los tests de regresión, que incluyen todos:

   ```bash
   pytest
   ```

### Ejecutar por tipo de testing:

Para ejecutar por tipo de prueba, utilice la opción `-m` de pytest junto con la marca correspondiente:
```bash
Ejm: pytest -m smoke
```

| Tipo Testing | Comando |
|--------|----------|
| Regression | `pytest` |
| Smoke | `pytest -m smoke` |
| Functional | `pytest -m functional_positive` |
| Negative | `pytest -m functional_negative` |
| Domain | `pytest -m domain` |

### Ejecutar por sub-módulo:

Para ejecutar por sub-módulo se puede combinar con los demás parámetros, agregando el directorio del submodulo:
```bash
Ejm: pytest .\tests\ -m smoke -v
```

| Módulo| Sub-módulo | Comando |
|-------|------------|---------|
| Catálogo | Taxons | `pytest .\tests\catalog\taxons\` |
| Catálogo | Taxons > Taxon Images | `pytest .\tests\catalog\taxons\taxon_images` |
| Iniciar Sesión | Autenticacion | `pytest .\tests\login\` |

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