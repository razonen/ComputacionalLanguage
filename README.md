# ComputacionalLanguage

Este software espera recibir un input que consiste en un conjunto de tweets reales 
en xml para intuir el género y el rango de edad del autor de dichos tweets.

Consiste en dos archivos, uno de training, al cual se le darán los tweets indicando su género y edad y entrenaremos
al algoritmo usando la herramienta de python "sklearn - SVM",
Y otro archivo de test, donde se le pasarán los tweets sin estar etiquetados, es decir, sin indicar el genero y edad del autor
y el ejecutable generará a partir del algoritmo entrenado una solución a cada tweet, es decir, har una predicción 
de género y edad del autor de los tweets dados.
