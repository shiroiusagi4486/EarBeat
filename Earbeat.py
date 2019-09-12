from Pipeline import  paginas, musical, caracteristicas, modeloreja, dendo, kmean, dedito, recomendacion, presentacion, nuevaRec


print('Es la primera vez que nos visitas?')
usuario = input('teclea S para si, n para No')
if usuario.upper() == 'S':
    print('Bienvenido a EarBeat, para generar las playlist que sean acordes a tu frecuencia cardiaca, te pediremos que introduzcas algunos datos y procesaremos otros, esto puede tomar algun tiempo, por favor se paciente')
    print("Estaremos avisandote de todo el proceso y gracias por utilizarnos")
    inicio = paginas()
    canciones = musical(inicio)
    informacion = caracteristicas(canciones)
    modelfix = modeloreja(informacion)
    dendograma = dendo(modelfix)
    clusters, kmean12 = kmean(modelfix)
    dedopromedio = dedito()
    recomendaciones = recomendacion(dedopromedio, clusters, kmean12, canciones)
    muestra = presentacion(recomendaciones)
else:
    print('Bienvenido nuevamente a continuacion elegiremos una nueva playlist basandonos en tu frecuencia cardiaca')
    print('Conecta tu sensor al dedo')
    dedopromedio = dedito()
    recomendaciones = nuevaRec(dedopromedio)
    muestra = presentacion(recomendaciones)