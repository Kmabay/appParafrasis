import pandas as pd
def Aproximadas(text1,text2,num):
    import re
    cadena1=re.split('\.',text1)
    cadena2=re.split('\.',text2)
    tabla=pd.DataFrame(data=[[1,1],[2,4],[3,9]], columns=['num','cuadrado'])
    
    return tabla
    #('\n\n'.join(map(str, cadenasI)))

res8=str(Aproximadas("todos ellos se componen de aromas. que simbolizan la purificación del alma. el aroma guía o atrae a los difuntos.podríamos decir que los platillos que se sirven. y forman parte. de la comida típica de méxico.me ha mordido un perro.texto4","otro componente es el aroma. que además de guiar a los difuntos. es la purificación del alma de los camoteros. ofrecen generalmente frutos de piel púrpura. y pulpa blanca. aunque también hay amarillos.me acaba de morder un can.texto8",10))
print(res8)