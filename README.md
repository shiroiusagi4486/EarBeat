# spoty-wero
La idea de este proyecto surge de una playlist colaborativa que tenemos dentro del bootcamp de data analytics de Ironhack, que debido a la diversidad de personas, resulta también bastante rara.

Por tanto, la idea fue el como poder hacer una playlist que contenga un poco de lo que todos escuchan

## Acercamiento al problema:

Cuando recien comence a explorar la pagina web para ver la estructura, no me percaté de que era una pagina web dinamica, entonces ese fue un inconveniente posterior porque tuve que el request me traia el script y por consiguiente ya no aparecen todas las playlist que se muestran en el navegador

Revisando el link del perfil de spotify, que contiene la estructura de https://open.spotify.com/user/ seguido del id de usuario de spotify, una interrogacion ? y numeros que no se repiten si reenvias el link.

usando ese link, pude realizar la busqueda de las playlist (algunas se muestran despues de la generacion de una pagina dinamica) pude traer el nombre de usuario y los nombres de las playlist, una vez establecido eso y como no queria que fuera de solo un usuario, decidi guardar todo dentro de una lista y así  puedes introducir de forma ilimitada los perfiles de usuario

Ya de data wrangling extraigo el id de usuario, los nombres de las playlist, las url de las mismasy genero el data frame que usaré para que el API de spotify me muestre las canciones que estan dentro de las playlist. Durante el proceso me encontre con un problema al querer establecer correctamente el dataframe, porque aunque las dimensiones de todas las listas son iguales entre si, son listas de listas y estas son variables, por tanto ahi me atoré un poco pero con la ayuda de mi Teacher (muchas gracias Osv), se resolvió ese problema sin inconveniente

Elgo que no noté es que no todas las canciones que se muestran en el data frame pueden ser leidas, supongo que se pueden hacer request para eliminarlas en caso de que no se puedan reproducir.

El Resultado final por el momento es un par de archivos csv donde se ven las playlist y los usuarios en uno y las canciones de todas las playlist involucradas

Para este proyecto aprendi a usar un poco más las expresiones regulares que realmente me cuestan un poco de trabajo, pero cada vez se va haciendo más sencillo construirlas, que la API de spotify es un relajo enorme porque no hay una estructura fija para toda su base de datos y algunos links no estan funcionales

## Mejoras futuras:

Limpieza del dataframe respecto a los duplicados y a si se puede o no ejecutar la canción en el navegador, sacar los outliers y crear una playlist colaborativa para que se pueda compartir con el resto de compañeros del bootcamp