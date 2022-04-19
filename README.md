# Mastermind

Prueba tecnica sobre el juego mastermind.

## Principales endpoints

Hay 5 endpoint principales, 2 en la ruta de user para el registro y login de 
usuarios y 3 en la ruta de game para jugar al juego en si, además hay otros endpoints
secundarios como el del panel de administración o el de la documentación.

### Listado de juegos disponibles:

GET `api/game/Boardgame/` sin parametros, devuelve el listado con los nombres 
 de los juegos

### Crear una nueva partida:

POST `/api/game/Game/` con los parametros requeridos `boardgame` y `user`, devuelve 
los datos de la partida creada

````json
{
    "id": 3,
    "finished": false,
    "winned": false,
    "max_guests": 10,
    "code": "",
    "user": 1,
    "boardgame": "Mastermind",
    "guests": []
} 
````

### Estado de la partida:

GET `/api/game/Game/2/` con el `id` de la partida como parametro en la ruta, nos 
 devuelve el estado de esta con todas las jugadas hasta ahora, como se ve a continuación

````json
{
    "id": 2,
    "finished": true,
    "winned": false,
    "max_guests": 10,
    "code": "",
    "user": 1,
    "boardgame": "Mastermind",
    "guests": [
        {
            "id": 14,
            "guest_code": "BBWW",
            "white_result": 1,
            "black_result": 1,
            "create_date": "2022-04-19T00:00:26.873712+02:00",
            "game": 2
        },
        {
            "id": 15,
            "guest_code": "BBWW",
            "white_result": 1,
            "black_result": 1,
            "create_date": "2022-04-19T00:06:06.980393+02:00",
            "game": 2
        }
    ]
}
````

### Hacer un intento de adivinar el código, una jugada

POST `/api/game/Guest/` con los parametros `guest_code` con el código a probar y 
 `game` con el id de la partida y devuelve los datos de la jugada incluido el 
 resultado, este es un ejemplo:

```json
{
    "id": 16,
    "guest_code": "BWWO",
    "white_result": 1,
    "black_result": 0,
    "create_date": "2022-04-19T15:19:39.224338+02:00",
    "game": 3
}
```

### Login:

POST `/api/users/auth/login/` con `username` y `password` como parámetros, 
devuelve el token jwt.

### Registro:

POST `/api/users/auth/register/` con `username`, `password`, `password2`
 y `email` como parametros, devuelve el username y el email si el registro 
se produce.

### Documentación:

GET `api/documentation/` nos permite acceder al swagger con la documentación del 
proyecto.

## Como desplegar el docker

Para poner en marcha el docker del proyecto simplemente hay que ejecutar 
los siguientes comandos.

```
docker-compose build
docker-compose run --rm app django-admin startproject core .
docker-compose up
```
## Questionario

- What is your favorite package manager and why?
> Mi gestor de paquetes favorito es pip, basicamente por su simplicidad y facilidad 
> de uso pero tambien uso mucho conda y anaconda ya que hago proyectos de Machine 
> Learning y Data Science y es lo mejor para tener las librerias agrupadas y a mano 
> aunque es bastante mas pesado.
- What architecture did you follow for this project?
> He utilizado el MVT clasico de Django. Para un proyecto tan pequeño era lo mejor 
> para desarrollarlo rápido, si fuera más grande hubiera usado DDD o CQRS.
- Do you know and understand UML? What would the class diagram of the domain 
exposed in the mastermind game be like for you?
> Si, los diagramas UML son una herramienta basica, de hecho hice el diagrama al 
> principio para entender como funcionaria y cuales serian las clases a implementar.
> El diagrama de clases para mi seria tal como la imagen que incluyo a continuación,
> La clase boardgame es una clase por si se quisiera en el futuro añadir más de un 
> juego, asimismo si se quisiera ampliar para no tener solo juegos de mesa crearia 
> una clase base abstracta para tipos de juego de la que heredaria boardgame, pero 
> me parecia inecesario en este momento. La clase Game representa las distintas 
> partidas y guarda el estado de estas y la clase Guest representa las jugadas o en 
> el caso de este juego los intento de adivinar la contraseña con el resultado de 
> cada intento.
> 
![Diagrama UML](/MastermindUML.jpg)
- What tools are you aware of to handle things like code styling and consistency, 
formatting, typing…?
> Yo utilizo el editor PyCharm que ya integra herramientas para mantener el formato 
> y cumplir los PEP de python, tambien uso extensiones para eso en Visual Studio Code 
> cuando lo utilizo. 
- Is there anything you would like to comment about the project, this small exercise, 
etc?
> Me hubiera gustado tener mas tiempo para dedicarle y pulir cosas, poner permisos 
> custom en los endpoints de la api, incluir todos los endpoints en la documentacion,
> hacer TDD. Aun asi para ser un proyecto tan pequeño me ha parecido muy interesante.