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
        '''
        data = [data2,data3]
        local_model_path = 'jfarray/Model_dccuchile_bert-base-spanish-wwm-uncased_50_Epochs'
        model = SentenceTransformer(local_model_path)
        
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
        return textdistance.tversky(data2,data3)

    dCoseno=round(cosenoS(format(req.form['dat1']),format(req.form['dat2'])),3)
    dDice=round(DiceS(format(req.form['dat1']),format(req.form['dat2'])),3)
    dJaccard=round(JaccardS(format(req.form['dat1']),format(req.form['dat2'])),3)
    dLev=LevS(format(req.form['dat1']),format(req.form['dat2']))
    dM1=round(Modelo1(format(req.form['dat1']),format(req.form['dat2'])),3)
    
    dM2=round(dM1-textdistance.monge_elkan(format(req.form['dat1']),format(req.form['dat2'])),3)

    return render_template("/App.html",textoA=format(req.form['dat1']),textoB=format(req.form['dat2']),resulta2=dCoseno,resulta3=dDice,resulta4=dJaccard,resulta5=dLev,resulta6=dM1,resulta7=dM2)

@app.route("/Distancia2",methods=["GET","POST"])
def Distancia2():
    import os
    import pandas as pd
    try:
        import textdistance
    except ModuleNotFoundError:
        os.system('pip install textdistance')
        import textdistance
    if req.method=="POST":
        text1=req.form["dat3"]
        text2=req.form["dat4"]
    
    def Aproximadas(text1,text2,Num):
        import re
        cadena1=re.split('\.',text1)
        cadena2=re.split('\.',text2)
        comparaciones = len(cadena1)*len(cadena2)
        combinaciones1=[]
        combinacionesO=[]
        oraciones=[]
        for j in range(len(cadena1)):
            for i in range(len(cadena2)):
                combinaciones1.append(textdistance.cosine(cadena1[j],cadena2[i]))
                combinacionesO.append(textdistance.cosine(cadena1[j],cadena2[i]))
                oraciones.append(str(cadena1[j]+" | "+cadena2[i]))
        combinacionesO.sort(reverse=True)
        Ncomb=[]
        Ncomb.append(combinacionesO[:Num])
        indices=[]
        for i in range(Num):
            indices.append(combinaciones1.index(Ncomb[0][i]))
        dato=[[1]*3 for j in range(Num)]
        for i in range(Num):
            dato[i]=i+1,round(Ncomb[0][i],3),oraciones[indices[i]]
        return dato


    numero=request.form['vol']
    headings = ("Lugar ","Medida","Textos comparados")
    data=Aproximadas(format(req.form['dat3']),format(req.form['dat4']),int(numero))
    #pd.DataFrame(Aproximadas(format(req.form['dat3']),format(req.form['dat4']),int(numero)), columns=['numero','cuadrado'])
    #str(Aproximadas(format(req.form['dat3']),format(req.form['dat4']),int(numero)))
    return render_template("/App.html",textoC=format(req.form['dat3']),textoD=format(req.form['dat4']),number=numero,headings=headings,data=data)#,resulta8=res8)



if __name__ == '__main__':
    app.debug=True
    app.run()