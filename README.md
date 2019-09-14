# Earbeat
La idea de este proyecto surge de una playlist colaborativa que tenemos dentro del bootcamp de data analytics de Ironhack, que debido a la diversidad de personas, resulta también bastante rara.

Por tanto, la idea fue el como poder hacer una playlist que contenga un poco de lo que todos escuchan. Sin embargo cuando una anecdota que cambió el enfoque resulta ser un encuentro casual en concierto gratuito en la glorieta de insurgentes de cierto grupo que me gusta escuchar, y en la emoción que sentí al estar escuchandolos en vivo, el aumento de los latidos de mi corazón. 

En ese momento se definió earbeat, como una aplicación que crea una playlist con canciones del propio usuario, utilizando la frecuencia cardica.

## Acercamiento al problema:

Cuando recien comence a explorar la pagina web  de open spotify, para ver la estructura, no me percaté de que era una pagina web dinamica, entonces ese fue un inconveniente posterior porque el request de beautiful soup me traia el script y por consiguiente ya no aparecen todas las playlist que se muestran en el navegador

Revisando el link del perfil de spotify, que contiene la estructura de https://open.spotify.com/user/ seguido del id de usuario de spotify, una interrogacion ? y numeros que no se repiten si reenvias el link, (Son generados dinamicamente).

Usando ese link, pude realizar la busqueda de las playlist (algunas se muestran despues de la generacion de una pagina dinamica), traer el nombre de usuario que ha creado la playlist y el nombre que le ha dado. Una vez establecido eso, decidi guardar todo dentro de una lista y crear un bucle para que puedas introducir de forma ilimitada los perfiles de usuario.

Ya de data wrangling extraigo el id de usuario, los nombres de las playlist, las url de las mismasy genero el data frame que usaré para que el API de spotify me muestre las canciones que estan dentro de las playlist. Durante el proceso me encontre con un problema al querer establecer correctamente el dataframe, porque aunque las dimensiones de todas las listas son iguales entre si, son listas de listas y estas son variables.

Algo de lo que pude percatarme, es que no todas las canciones que se muestran en el dataframe, cuando tienes a usuarios internacionales es que las canciones estan restringidas a ciertos paises y pueden ser escuchadas en otros.

El último paso fue conseguir las audio features de cada cancion, este proceso fue lento, pero es debido más que nada a la velocidad de internet, se hizo la prueba y pude obtener 1744 features desde 2 hasta 4 veces (Ya en la ejecucion del programa solo se necesitará extraer una sola vez las audio features, por lo que solo se necesita de una buena velocidad para que no tarde tanto)

### Lectura de pulso cardiaco

La primera idea que surgio para hacer la lectura del pulso cardiaco, fue mediante un sensor bluetooth de la marca polar, que ya hace esa función y obtener solamente la frecuencia, usando para eso un raspberry 3a+, junto con la libreria de bluepy, sin embargo por cuestion de tiempo, se cambió del sensor bluetooth y del raspberry a un sensor (oximetro) mucho más sencillo y un arduino one, y programar la recepción de las mediciones de frecuencia cardiaca tanto en arduino como en python, usando la libreria serial, el último paso fue crear el archivo .py, para poder usarlo como otra libreria.

### 

## Mejoras futuras:
