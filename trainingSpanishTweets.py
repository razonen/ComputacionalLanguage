# ComputacionalLanguage
# -*- coding: 850 -*-
#!/usr/bin/env python
import os
import sys
###################   AUTHOR PROFILING

#tratamiento del fichero xml
def copiar_fichero(filename):
	f =  open(filename,"r")
	text = ""
	for linea in f.readlines():
		if  linea.find('CDATA[') > -1:
				#numT = numT + 1
				text = text + linea
	f.close()
	return text

#inicializamos la matriz de variables
def inicializa_matriz(fils, cols):
	m = [None] * fils
	for i in range(fils):
		m[i] = [None] * cols
	return m

#contamos el numero de tweets que tiene el archivo
def cuenta_num_tweets(string):
	numT = 0 
	for linea in string.split('\n'):
		if linea.find('CDATA[') > -1:
			numT = numT + 1
	return numT

def linea_valida(linea):
	vale = False 
	if  linea.find('CDATA[') > -1 :
		vale = True
	return vale

def filtrar_linea(linea):
	#print "TWEET SIN FILTRAR"
	#print linea
	tweet = ""
	num  = -1
	num = linea.find('CDATA[')

	#if linea.find('</document>') > -1 :
	#	num2 = linea.find('</document>')
	ind = 1
	linea2 = linea[num+6:]
	num2 = num+6
	for l in linea2:
		if l == '[':
			ind += 1
		elif l == ']':
			ind -=1
		if ind == 0:
			break
		num2 += 1
	if num > -1 and num2 > -1:
		num = num + 6 
		num2 = num2 
		tweet = linea[num:num2]
	#print "TWEET FILTRADO: "
	#print tweet
	return tweet

def contar_referecias(tweet):
	num = tweet.count("<a" or "<img" or "<![C")
	return num

def quitar_referencias(tweet):
	num_refer1 = tweet.count("<a")
	num_refer2 = tweet.count("<img")
	num_refer3 = tweet.count("<![C")
	for r in range(num_refer1):
		ind  = -1
		inicioRefer = tweet.find('<a')
		finRef = tweet.find('</a>',inicioRefer)
		tweet = tweet[:inicioRefer] + tweet[finRef+4:]
	for s in range(num_refer2):
		ind  = -1
		inicioRefer = tweet.find('<img')
		finRef = tweet.find('>',inicioRefer)
		tweet = tweet[:inicioRefer] + tweet[finRef+1:]
	for t in range(num_refer3):
		ind  = -1
		inicioRefer = tweet.find('<![C')
		finRef = tweet.find('>',inicioRefer)
		tweet = tweet[:inicioRefer] + tweet[finRef+1:]
	return tweet


def quitar_signos(tweet):
	punt = (',' , '.' , ':','[',']','(',')','-','--',';','!','','?','\"','\'','\`','\'\'', '``','`', '\n')
	punt = punt + ('@','#','&')
	new_str = ""
	for w in tweet:
		if w not in punt:
			#print ("letra aceptada:[{}]".format(w) )
			new_str = new_str + w.lower()
	return new_str


def numero_palabras(tweet):
		cadena = tweet.split()
		num_de_palabras = len(cadena)
		return num_de_palabras	

def numero_caracteres(tweet):
		cadena = tweet.split()
		num_de_caract = 0
		for x in cadena:
			num_de_caract = num_de_caract +  len(x)
		return num_de_caract	

def rellena_matriz(m, palabras_totales, caracteres_totales, numero_d_refer, numT, numTweets, tweet):

	m[numT][0] = palabras_totales
	m[numT][1] = caracteres_totales
	m[numT][2] = numero_d_refer
	return  m

def contiene_tweets(ruta):
	if os.path.exists(ruta) == False:
		sys.exit("ERROR: this path does not exist : {}".format(ruta) )
	texto = copiar_fichero(ruta)
	numero = cuenta_num_tweets(texto)
	return numero

def obtener_genero(rutaSol, perfil):

	f =  open(rutaSol,"r")
	texto = ""
	for linea in f.readlines():
		texto = texto + linea
	f.close()
	existePerfil = False
	genero = ""
	for linea in texto.split('\n'):
		if linea.find(perfil) > -1 :
			existePerfil = True
			if linea.find("FEMALE") > -1:
				genero = "FEMALE"
			else:
				genero =  "MALE"
	if existePerfil == True :
		return genero
	else:
		print (" ERROR : NO MALE and NO FEMALE: {}".format(perfil) )
		return "NO MALE NO FEMALE"

def obtener_edad(rutaSol, perfil):

	f =  open(rutaSol,"r")
	texto = ""
	for linea in f.readlines():
		texto = texto + linea
	f.close()
	existePerfil = False
	edad = ""
	for linea in texto.split('\n'):
		if linea.find(perfil) > -1 :
			existePerfil = True
			if linea.find("18-24") > -1:
				edad = "18-24"
			elif linea.find("25-34") > -1:
				edad = "25-34"
			elif linea.find("35-49") > -1:
				edad = "35-49"
			elif linea.find("50-64") > -1:
				edad = "50-64"
			elif linea.find("65-xx") > -1:
				edad = "65-xx"

	if existePerfil == True :
		return edad
	else:
		print (" ERROR :  THERE IS NOT AGE in: {}".format(perfil))
		return "NO AGE"

def rellena_vector (diccionar, palabras_totales):
	ind = 0 
	sumatorio = 0  
	vector_final = [0]*len(diccionario_general2)
	for bigrama in diccionario_general2:
		if bigrama in diccionar:
			sumatorio += 1
			vector_final[ind] = round ( (diccionar[bigrama]+1) / palabras_totales  , 7 )
		else:
			vector_final[ind] = 0
		ind = ind + 1
	#print ("sumatorio de palabras = ", sumatorio)
	#print ("len(diccionar) = ", len(diccionar))
	return vector_final


def rellena_diccionario (tweet, diccionar):
	tweet_list = tweet.split(" ")
	longit = len(tweet_list)
	for j in range (longit):
		if j == 0:
			bigrama = ('<S>',tweet_list[j])
			if bigrama not in diccionar:
				diccionar[bigrama] = 1
			else:
				diccionar[bigrama] += 1
		elif j == longit-1:
			bigrama = ('</S>',tweet_list[j])
			if bigrama not in diccionar:
				diccionar[bigrama] = 1
			else:
				diccionar[bigrama] += 1
		else:
			bigrama = (tweet_list[j], tweet_list[j+1])
			if bigrama not in diccionar:
				diccionar[bigrama] = 1
			else:
				diccionar[bigrama] += 1
	return diccionar


##################################################################################


def profile_xml (archivo):
	diccionar = {}
	texto = copiar_fichero(archivo)
	numTweets = cuenta_num_tweets(texto)
	#print ("{}  ---->>>  tiene {} tweets".format(archivo[-7:], numTweets) )
	m = inicializa_matriz(numTweets,3)
	palabras_totales = 0.0
	caracteres_totales = 0.0
	referencias_totales = 0.0
	numT = 0.0
	for linea in texto.split('\n'):
		if (linea_valida(linea)):
			tweet = filtrar_linea(linea)
			numero_d_refer = contar_referecias(tweet)
			tweet = quitar_referencias(tweet)
			tweet = quitar_signos(tweet)
			#print tweet
			num_de_palabras = numero_palabras(tweet)
			num_de_caracteres = numero_caracteres(tweet)
			if num_de_palabras > 3:
				rellena_diccionario (tweet, diccionar)
				palabras_totales = num_de_palabras + palabras_totales +1
				caracteres_totales = num_de_caracteres + caracteres_totales
				referencias_totales =  numero_d_refer + referencias_totales
				numT = numT + 1
				riqueza_diccionario = 0
				for p in diccionar:
					riqueza_diccionario = riqueza_diccionario + diccionar[p]
				#if (palabras_totales !=  riqueza_diccionario ):
					#print ("totales: {}  riqueza_diccionario {}: ".format(palabras_totales, riqueza_diccionario ))
					#print (diccionar)
					#sys.stderr("ERROR ERROR ERROR TYPE 1")
	riqueza_vocabulario = 0.0
	total = 0.0
	riqueza_vocabulario = len(diccionar)
	vector_final = rellena_vector(diccionar, palabras_totales )
	for elem in vector_final:
		total += elem

	#print (len(vector_final))
	vector_final.append( round( referencias_totales/numT , 5)   )
	vector_final.append(  round( palabras_totales/numT ,5  ) )
	vector_final.append( round ( caracteres_totales/numT , 5 ) )
	vector_final.append( round ( riqueza_vocabulario/palabras_totales , 5 ) )
	#print ("************ DICCIONARIO ************")
	return vector_final

#########################################################################################

def crear_matriz_caracteristicas(direccion_base):
	i = 0
	numFiles = 0
	for base, dirs, files in os.walk(direccion_base):
		numFiles = numFiles + 1
	if numFiles < 1:
		print ("ERROR {} has 0 files: ".format(direccion_base))
		print direccion_base
		return 0
	for base, dirs, files in os.walk(direccion_base):
		print "BASE: "
		print base
		print "DIRS: "
		print dirs
		print "FILES: "
		print files

		solo3 = 0
		for i in files:

			ruta = direccion_base + i
			if contiene_tweets(ruta) > 1:
				vectorID = profile_xml(ruta)
				vectorID.insert(0,i[:-4])
				ruta_sol = direccion_base + "truth.txt"
				rangoEdad = obtener_edad(ruta_sol, i[:-4])
				genero = obtener_genero(ruta_sol, i[:-4]) 
				vectorID.append(genero)
				vectorID.append(rangoEdad)
				matriz.append(vectorID)
				if solo3 < 3:
					print "genero obtenido: {}".format(genero)
					print "rangoEdad obtenido: {}".format(rangoEdad)
					print "ruta : {}".format(ruta)
				solo3 += 1 
			else:
				print ("  esta URL no tiene tweets accesibles: {}".format(ruta))

	numF = len(matriz)
	numC = len(matriz[0])
	print ("tamanyo matriz: {}, {}".format(numF, numC))
	print (" MATRIZ SIMPLIFICADA: ")
	show = 0
	for fil in matriz :
		if show	< 5 :
			print (fil[0],"...",fil[1],fil[2],fil[3],"...",fil[numC-10],fil[numC-9],fil[numC-8],fil[numC-7],"...",fil[numC-6],fil[numC-5],fil[numC-4],fil[numC-3],fil[numC-2],fil[numC-1])
			show += 1
#####################################################################################################

def training_gender(matriz, output):

	from sklearn import svm
	from sklearn import datasets

	print ("START TRAINING GENDER")
	print ("Size of Matrix of features: {}x{} ".format(len(matriz), len(matriz[0]) ) )
	sizeMatrix = float(len(matriz))

	vectorSol = [ col[-2] for col in matriz ]
	matrizSinSol = [ col[1:-2] for col in matriz ]
	
	print ("LEN of vector Solucion:  {} ".format(len(vectorSol) ) )  
	print ("SIZE of matriz Sin Solucion : {}x{}  ".format( len(matrizSinSol) , len(matrizSinSol[0] ) ) )

	clf = svm.SVC(gamma=0.001, C=100.)

	if len(matrizSinSol) == len(vectorSol):
		clf.fit(matrizSinSol, vectorSol)

		from sklearn.externals import joblib

		path = output + "/ML_spanish_GENDER/"
		if os.path.isdir( path ) == False:
			os.mkdir( path )
		ML_path = path + "/ml.pkl"
		joblib.dump(clf, ML_path)

		print ("MODEL LANGUAGE CREATED FOR spanish AND gender in " + path)

	else: 
		sys.exit("ERROR ERROR ERROR : VECTOR with solutions have different SIZE than matrix without solutions")

	print ("FINISH TRAINING GENDER")
	print ("*****")
######################################################################################

def training_age(matriz, output):

	from sklearn import svm
	from sklearn import datasets

	print ("START TRAINING AGE")
	print ("Size of Matrix of features: {}x{} ".format(len(matriz), len(matriz[0]) ) )
	sizeMatrix = float(len(matriz))

	vectorSol = [ col[-1] for col in matriz ]
	matrizSinSol = [ col[1:-2] for col in matriz ]
	
	print ("LEN of vector Solucion:  {} ".format(len(vectorSol) ) )  
	print ("SIZE of matriz Sin Solucion : {}x{}  ".format( len(matrizSinSol) , len(matrizSinSol[0] ) ) )

	clf = svm.SVC(gamma=0.001, C=100.)

	if len(matrizSinSol) == len(vectorSol):
		clf.fit(matrizSinSol, vectorSol)

		from sklearn.externals import joblib

		path = output + "/ML_spanish_AGE/"
		if os.path.isdir( path ) == False:
			os.mkdir( path )
		ML_path = path + "/ml.pkl"
		joblib.dump(clf, ML_path)

		print ("MODEL LANGUAGE CREATED FOR spanish AND age in " + path)

	else: 
		sys.exit("ERROR ERROR ERROR : VECTOR with solutions have different SIZE than matrix without solutions")

	print ("FINISH TRAINING AGE")
	print ("*****")
######################################################################################

def anyadir_bigrama(pal1, pal2):
	bigrama = (pal1,pal2)
	if  bigrama not in diccionario_general:
		diccionario_general[bigrama] = 1
	else:
		diccionario_general[bigrama] += 1

def rellena_dic_gen(str):

	direccion_base = str
	numFiles = 0
	for base, dirs, files in os.walk(direccion_base):
		print ("cuantos archivos (files): ", len(files) )
		#numFiles = numFiles + 1
		#print (files)

	if len(files) < 1:
		print ("ERROR, DIRECTORY with 0 files")
		return 0
	numFiles = len(files)
	#print ("numero de archivos en {} = {}".format(str,numFiles) )
	print ("START    creamos diccionario_general")	
	for base, dirs, files in os.walk(direccion_base):
		#print (files)
		for i in files:
			#print ("")
			ruta = direccion_base + i
			#print ("ruta = {}".format(ruta) )
			if contiene_tweets(ruta) > 1:
				texto = copiar_fichero(ruta)
			for linea in texto.split('\n'):
				if (linea_valida(linea)):
					tweet = filtrar_linea(linea)
					tweet = quitar_referencias(tweet)
					tweet = quitar_signos(tweet)
					num_de_palabras = numero_palabras(tweet)
					if num_de_palabras > 3:
						tweet_list = tweet.split(" ")
						longit = len(tweet_list)
						for j in range (longit):
							if j == 0:
								anyadir_bigrama('<S>',tweet_list[j])
							elif j == longit-1:
								anyadir_bigrama(tweet_list[j],'</S>')
							else:
								anyadir_bigrama(tweet_list[j], tweet_list[j+1])
	repetDicGen = 0
	repetDicGen2 = 0
	for p in diccionario_general:
		if diccionario_general[p] > 6:
			diccionario_general2[p] = diccionario_general[p]
	for p in diccionario_general:
		repetDicGen += diccionario_general[p]
	for p in diccionario_general2:
		repetDicGen2 += diccionario_general2[p]
	print ("FINISH  diccionario_general creado **** {} bigramas diferentes *** {} contando repeticiones".format(len(diccionario_general),repetDicGen) )
	print ("diccionario_general longitud: ", len(diccionario_general) )
	print ("FINISH   diccionario_general 2 creado **** {} bigramas diferentes *** {} contando repeticiones".format(len(diccionario_general2),repetDicGen2) )
	print ("diccionario_general longitud: ", len(diccionario_general2) )
	return 1


#######################################################################################################

def  guarda_diccionario_gen(output):
	path = output + "/dic_spa.txt"
	f = open( path ,"w")
	for p,q in diccionario_general2:
		f.write(p + " " + q +'\n')
	f.close()


##################################################################################
#### MAIN ###
if (len(sys.argv)  == 5) :
	if  (sys.argv[1] == '-c' or sys.argv[1] == '-C') and (sys.argv[3] == '-o' or sys.argv[3] == '-O') or (sys.argv[3] == '-c' or sys.argv[3] == '-C') and (sys.argv[1] == '-o' or sys.argv[1] == '-O'):  
		if (sys.argv[1] == '-c' or sys.argv[1] == '-C') :
			inputDataSet = sys.argv[2]
			outputDataSet = sys.argv[4]
		else:
			inputDataSet = sys.argv[4]
			outputDataSet = sys.argv[2]
		print ("Number of parameters: ", len(sys.argv) )
		print ("List of parameters: ", sys.argv )
		print ("Directory with DATASET to TRAIN: {} ".format( inputDataSet ) ) 
		print ("Directory to save dictionary and ML: ".format( outputDataSet ) )
		diccionario_general = {}
		diccionario_general2 = {}
		command  = "mkdir -p " + outputDataSet
		print (command)
		os.system(command)
		command = "ls"
		print command
		os.system(command)
		if (rellena_dic_gen( inputDataSet +'/') == 1):
			guarda_diccionario_gen( outputDataSet )
			matriz = []
			crear_matriz_caracteristicas(inputDataSet+'/')
			if len(matriz) > 1:
				training_gender(matriz,outputDataSet)
				training_age(matriz, outputDataSet)
			else:
				sys.exit("ERROR ERROR ERROR : NO DATA TO TRAIN")
		else:
			 sys.exit("ERROR ERROR ERROR : No tweets in this Dir") 
		#comando = "tar -cvf " + outputDataSet + ".tar "  + outputDataSet 
		#print comando
		#os.system(comando)
	else:
		print ("ERROR INPUT (2)")
		print ("To execute TrainSpanish6.py :")
		print ("python TrainSpanish8.py -c inputDataSet/ -o outputDir/")		
else:
	print ("ERROR INPUT (1)")
	print ("To execute TrainSpanish8.py :")
	print ("python TrainSpanish8.py -c inputDataSet/ -o outputDir/")

