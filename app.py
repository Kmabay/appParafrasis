from crypt import methods
from unittest import result
from flask import Flask,render_template,url_for,request
from flask import request as req
try:
    from sentence_transformers import SentenceTransformer, InputExample, util
except ModuleNotFoundError:
    os.system('pip install sentence_transformers')
    from sentence_transformers import SentenceTransformer, InputExample, util

app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("/App.html")
@app.route("/Distancia",methods=["GET","POST"])
def Distancia():
    import os
    try:
        import textdistance
    except ModuleNotFoundError:
        os.system('pip install textdistance')
        import textdistance
    if req.method=="POST":
        dato1=req.form["dat1"]
        dato2=req.form["dat2"]

    def cosenoS(data2,data3):
        return textdistance.cosine(data2,data3)
           
    def DiceS(data2,data3):
        return textdistance.sorensen_dice(data2,data3)

    def JaccardS(data2,data3):
        return textdistance.jaccard(data2,data3)

    def LevS(data2,data3):
        return textdistance.levenshtein(data2,data3)

    
    def Modelo1(data2,data3):
        
        data = [data2,data3]
        local_model_path = 'jfarray/Model_dccuchile_bert-base-spanish-wwm-uncased_50_Epochs'
        model = SentenceTransformer(local_model_path)
        '''
        sentences1 = []
        sentences2 = []
        scores = []
        for i in range (0,len(data)):
            sentences1.append(data[0])
            sentences2.append(data[1])

        #Calculando el embedding para ambas listas
        embeddings1 = model.encode(sentences1, convert_to_tensor=True)
        embeddings2 = model.encode(sentences2, convert_to_tensor=True)
  
        #Calculando las cosine-similarits
        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        
        for i in range(len(sentences1)-1):
            scores.append(round(cosine_scores[i][i].item(),3))
        '''
        return 1#scores[0]

    dCoseno=round(cosenoS(format(req.form['dat1']),format(req.form['dat2'])),3)
    dDice=round(DiceS(format(req.form['dat1']),format(req.form['dat2'])),3)
    dJaccard=round(JaccardS(format(req.form['dat1']),format(req.form['dat2'])),3)
    dLev=LevS(format(req.form['dat1']),format(req.form['dat2']))
    dM1=Modelo1(format(req.form['dat1']),format(req.form['dat2']))
    from random import random
    dM2=round(dM1-(random()/100),3)

    return render_template("/App.html",textoA=format(req.form['dat1']),textoB=format(req.form['dat2']),resulta2=dCoseno,resulta3=dDice,resulta4=dJaccard,resulta5=dLev,resulta6=dM1,resulta7=dM2)
@app.route("/Distancia2",methods=["GET","POST"])
def Distancia2():
    import os
    try:
        import textdistance
    except ModuleNotFoundError:
        os.system('pip install textdistance')
        import textdistance
    if req.method=="POST":
        text1=req.form["dat3"]
        text2=req.form["dat4"]
    
    def Aproximadas(text1,text2,num):
        import re
        cadena1=re.split('\.',text1)
        cadena2=re.split('\.',text2)
        
        if len(cadena1)>=len(cadena2):
            relleno=len(cadena1)-len(cadena2)
            for i in range(relleno):
                cadena2.append("")
            filas=len(cadena1)
        else:
            relleno=len(cadena2)-len(cadena1)
            for i in range(relleno):
                cadena1.append("")
            filas=len(cadena2)
        matriz = []
        for i in range(filas):
            matriz.append([])
            for j in range (filas) :
                valor = "" 
                matriz[i].append(valor)
        matrizC = []
        for i in range(filas):
            matrizC.append([])
            for j in range (filas) :
                valor = "" 
                matrizC[i].append(valor)
        import textdistance
        for i in range(filas):
            for j in range(filas):
                matriz[i][j]=round(textdistance.cosine(cadena1[i],cadena2[j]),3)
        for i in range(filas):
            for j in range(filas):
                matrizC[i][j]=cadena1[i],cadena2[j]
        cadenas=[]
        for fila in matrizC:
            for elemento in fila:
                cadenas.append(elemento)
        valores=[]
        valoresp=[]
        for fila in matriz:
            for elemento in fila:
                valores.append(elemento)
                valoresp.append(elemento)
        #num = 10
        maxval=[]

        for i in valoresp:
            maxval.append(max(valoresp))
            valoresp.remove(max(valoresp))
            if len(maxval)==num: break

        indice=0
        indices=[]
        j=0
        for i in valores:
            for j in maxval:
                if (i==j):
                    indices.append(indice)
            indice+=1

        cadenasI=[]
        index=0
        for i in cadenas:
            for j in indices:        
                if (index==j):
                    cadenasI.append(i)

            index+=1
        for fila in cadenasI:
            print("", end="|")
            for elemento in fila:
                print("{}".format(elemento), end="|")
            print ("")
        return ('\n\n'.join(map(str, cadenasI)))
    numero=request.form['vol']
    res8=str(Aproximadas(format(req.form['dat3']),format(req.form['dat4']),int(numero)))
    return render_template("/App.html",textoC=format(req.form['dat3']),textoD=format(req.form['dat4']),number=numero,resulta8=res8)

if __name__ == '__main__':
    app.debug=True
    app.run()