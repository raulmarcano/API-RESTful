
# API REST para la Gestión de Clientes y Simulaciones de Hipotecas

Este proyecto proporciona una **API REST** para gestionar clientes y realizar simulaciones de hipotecas. La API permite agregar, actualizar, obtener, eliminar clientes y simular hipotecas basadas en los datos proporcionados.

## Documentación

La API proporciona documentación interactiva generada automaticamente por **FastAPI**. Puedes acceder a la documentación en tiempo real a través de la siguiente URL:

`http://localhost:8000/docs`

## Funcionalidades

### Gestión de Clientes
- **Agregar cliente**: Permite almacenar la información de un cliente, incluyendo nombre de usuario, correo electrónico, NIF y el capital solicitado.
- **Actualizar cliente**: Permite actualizar la información de un cliente existente en la base de datos.
- **Obtener cliente por NIF**: Permite consultar la información de un cliente proporcionando su NIF.
- **Eliminar cliente**: Elimina un cliente.

### Simulación de Hipotecas
- **Simular hipoteca**: Realiza una simulación de hipoteca calculando la cuota mensual y el total a pagar según el capital, la tasa anual efectiva (TAE) y el plazo (en años).

## Requisitos
- Python 3.12.4 o superior.
- FastAPI
- Uvicorn
- SQLite

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/raulmarcano/API-RESTful.git
   ```

2. En la carpeta raíz, ejecuta el siguiente comando para instalar las dependecias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación con `uvicorn`:
   ```bash
   uvicorn main:app --reload
   ```

   Esto iniciará el servidor en `http://localhost:8000`.

## Estructura de la Base de Datos
La base de datos está compuesta por dos tablas principales: `clients` y `mortgage_simulations`.

### `clients`
Almacena la información de los clientes, con los siguientes campos:
- `id`: Identificador único del cliente.
- `username`: Nombre completo del cliente.
- `email`: Correo electrónico único del cliente.
- `nif`: NIF del cliente (DNI o NIE), único.
- `capital`: Capital solicitado por el cliente.

### `mortgage_simulations`
Almacena las simulaciones de hipotecas relacionadas con los clientes. Los campos son:
- `id`: Identificador único de la simulación.
- `nif`: NIF del cliente.
- `capital`: Capital solicitado por el cliente para la hipoteca.
- `tae`: Tasa Anual Equivalente.
- `years`: Número de años del préstamo.
- `monthly_pay`: Pago mensual de la hipoteca.
- `total`: Total a pagar al final del préstamo.


## Endpoints
### 1. `GET /`
- **Descripción**: Ruta de prueba para verificar que la API está funcionando.
- **Respuesta**:
  ```json
  {
    "message": "It´s aliveee!"
  }
  ```

### 2. `POST /add_client`
- **Descripción**: Permite agregar un nuevo cliente a la base de datos.
- **Cuerpo de la solicitud**:
```json
{
    "username": "Joaquin Phoenix",
    "email": "Phoenix@example.com",
    "nif": "12345678A",
    "capital": 150000
}
```
> [!IMPORTANT]
> - Se comprueba que el NIF contenga la letra correcta por el algoritmo oficial. 
> - El NIF acepta letras minúsculas y las transforma a mayúsculas pero no acepta formatos con guiones o espacios: 55127345-C❌ Y-1234567.N❌
> - Se comprueba que el email tenga un formato de correo válido.

- **Respuestas**:
  - 200: Cliente agregado exitosamente.
  - 400: El NIF o correo electrónico ya existe.
  - 422: Datos inválidos (por ejemplo, formato incorrecto de NIF).

### 3. `POST /update_client`
- **Descripción**: Permite actualizar los datos de un cliente existente.
- **Cuerpo de la solicitud**: Igual que en `POST /add_client`.
- **Respuestas**:
  - 200: Cliente actualizado correctamente.
  - 404: El cliente no fue encontrado.
  - 422: Datos inválidos.

### 4. `GET /get_client`
- **Descripción**: Permite obtener los datos de un cliente a partir de su NIF.
- **Parámetro por Query**: `nif` (obligatorio).
- **Respuestas**:
  - 200: Información del cliente.
  - 404: Cliente no encontrado.
  - 422: Formato de NIF inválido.

### 5. `POST /simulate_mortgage`
- **Descripción**: Realiza una simulación de hipoteca para un cliente.
- **Parámetros por Query**:
  - `nif`: NIF del cliente.
  - `tae`: Tasa Anual Equivalente (TAE).
  - `years`: Número de años para el préstamo.
- **Respuestas**:
  - 200: Información de la simulación (cuota mensual y total).
  - 404: Cliente no encontrado.
  - 422: Datos inválidos (TAE o años).

### 6. `DELETE /delete_client`
- **Descripción**: Elimina un cliente y todas sus simulaciones de hipoteca.
- **Parámetro por Query**: `nif` (obligatorio).
- **Respuestas**:
  - 200: Cliente eliminado exitosamente.
  - 404: Cliente no encontrado.
  - 422: NIF inválido.


## Modelos de Datos

### `ClientModel`
El modelo que define la estructura de los clientes:  (utiliza `Pydantic` para la validación de datos en las solicitudes)

```python
class ClientModel(BaseModel):
    username: str = Field(..., title="Username", description="Full name of the client", max_length=50)
    email: EmailStr = Field(..., title="Email", description="Unique email address of the client")
    nif: str = Field(..., title="NIF", description="Unique National identifier (DNI or NIE) of the client", min_length=8, max_length=12)
    capital: float = Field(..., title="Requested Capital", description="Amount of money requested by the client", gt=0)
```
