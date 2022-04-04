# -*- coding: utf-8 -*-
"""Entrega1_HavensteinButtazzoni

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19SnTqToOwqeIykHhSY9W-xODkMNEzWJ2
"""

#link KAGGLE - https://www.kaggle.com/rikdifos/credit-card-approval-prediction?select=credit_record.csv

"""**PROYECTO FINAL CURSO DATA SCIENCE CODERHOUSE 2022**

Trabajaremos sobre un dataset de TARJETAS DE CRÉDITO con el objetivo de definir clusters de clientes centrándonos en la posibilidad de cobro ante los mismos. Entonces, de esta forma, tendremos una cluesterización de clientes que permita a la empresa verificar si éste sera un cliente cumplidor o no.
"""

#Importamos librerías
import pandas as pd
import numpy as np
import seaborn as sns
from seaborn import distplot
import matplotlib.pyplot as plt

#Leemos los dataset
aplication = pd.read_csv("/content/application.csv")
aplication

#Leemos los dataset
credit = pd.read_csv("/content/credit.csv")
credit

#Unimos los dataset
df = pd.merge(aplication,credit,on="ID")
df

"""En los siguientes pasos se realizará un análisis EDA para identificar variables y su comportamiento"""

#Vemos resumen del dataset
df.describe().round().T

#Reemplazo los valores str por int en "ACCOUNT STATUS"
df= df.replace({"C":"6","X":"7"})
df

#Vemos el tamaño
df.shape

#Vemos nombre de columnas
df.columns

#Cambiamos nombres de columnas
df = df.rename(columns={"CODE_GENDER":"GENDER", "FLAG_OWN_CAR":"CAR","FLAG_OWN_REALTY":"PROPERTIES","CNT_CHILDREN":"CHILDREN", "AMT_INCOME_TOTAL":"ANNUAL INCOME", "NAME_INCOME_TYPE":"INCOME CATEGORY", "NAME_EDUCATION_TYPE":"EDUCATION LEVEL", "NAME_FAMILY_STATUS":"MARITAL STATUS", "NAME_HOUSING_TYPE":"WAY OF LIVING", "DAYS_BIRTH":"BIRTHDAY", "DAYS_EMPLOYED":"START DAY", "FLAG_MOBIL":"MOBILE PHONE", "FLAG_WORK_PHONE":"WORK PHONE", "FLAG_PHONE": "PHONE", "FLAG_EMAIL": "EMAIL", "OCCUPATION_TYPE":"OCCUPATION", "CNT_FAM_MEMBERS":"FAMILY SIZE", "MONTHS_BALANCE":"MONTHS OF BALANCE", "STATUS":"ACCOUNT STATUS"})
df

"""Se cambió el nombre de las columnas para una mayor identificación de las variables. 
A continuación, se hará una breve descripción de ellas:

**ID:** Numero de cliente

**GENDER:**	Género del cliente.

**CAR**	posee o no auto

**PROPERTIES**	posee propiedades

**CHILDREN**	Numero de niños	

**ANNUAL INCOME** Ingresos anuales

**INCOME CATEGORY**	Categoría de ingresos	

**EDUCATION TYPE** Nivel de Educación	

**MARITAL STATUS**	Estado civil	

**WAY OF LIVING**	Modo de vivir	

**BIRTHDAY**	Cumpleaños - Cuenta hacia atrás desde el día actual (0), -1 significa ayer,etc.

**START DAY**	Fecha de inicio del empleo	Contar hacia atrás desde el día actual (0). Si es positivo, significa la persona actualmente desempleada.

**MOBILE PHONE** Posee telefono movil

**WORK PHON**E	Posee teléfono de trabajo

**PHONE**	Posee teléfono

**E-MAIL** hay un correo electronico	

**OCCUPATION**	Ocupación	

**FAMILY SIZE**	Tamaño de la familia	

**MONTHS OF BALANCE**	El mes de los datos extraídos es el punto de partida, al revés, 0 es el mes actual, -1 es el mes anterior, etc.

**ACCOUNT STATUS**
0: 1-29 días de atraso 
1: 30-59 días de atraso 
2: 60-89 días de atraso 
3: 90-119 días de atraso 
4: 120-149 días de atraso 
5: Deudas atrasadas o incobrables, canceladas por más de 150 días 
C: pagado ese mes 
X: No hay préstamo para el mes
"""

df.value_counts("ACCOUNT STATUS")

#Vemos tipos de datos de cada columna
df.dtypes

#Vemos info sobre null
df.info()

#Eliminamos NaN
df.isnull().sum()

df_limpio = df.dropna()
df_limpio

#Vemos cual es la ocupación mas popular
df_limpio.value_counts("OCCUPATION")

#Vemos cual es la forma de vida mas popular
df_limpio.value_counts("WAY OF LIVING")

#Vemos cual es el nivel de educación mas popular
df_limpio.value_counts("EDUCATION LEVEL")

#Vemos cual es la categoria de ingresos mas popular
df_limpio.value_counts("INCOME CATEGORY")

df_limpio.value_counts("ANNUAL INCOME").sort_index()

#Se generan rangos para la columna "Annual Income" para facilitar el análisis

#REFERENCIAS: 1(entre  0y 100.000), 2(entre  100Ky 200K), 3(entre  200Ky 300K), 4(entre 300Ky 400K), 5(entre  400Ky 500K), 6(entre  500Ky 600K), 7(entre  600Ky 700K)
#8(entre  700Ky 800K), 9(entre  800Ky 900K), 10(entre  900Ky 1M), 11(entre 1M y 1.5M), 12(entre 1.5M y 2M)

conditions = [
    (df_limpio["ANNUAL INCOME"]> 0) & (df_limpio["ANNUAL INCOME"]<= 100000),
    (df_limpio["ANNUAL INCOME"]> 100000) & (df_limpio["ANNUAL INCOME"]<= 200000),
    (df_limpio["ANNUAL INCOME"]> 200000) & (df_limpio["ANNUAL INCOME"]<= 300000),
    (df_limpio["ANNUAL INCOME"]> 300000) & (df_limpio["ANNUAL INCOME"]<= 400000),
    (df_limpio["ANNUAL INCOME"]> 400000) & (df_limpio["ANNUAL INCOME"]<= 500000),
    (df_limpio["ANNUAL INCOME"]> 500000) & (df_limpio["ANNUAL INCOME"]<= 600000),
    (df_limpio["ANNUAL INCOME"]> 600000) & (df_limpio["ANNUAL INCOME"]<= 700000), 
    (df_limpio["ANNUAL INCOME"]> 700000) & (df_limpio["ANNUAL INCOME"]<= 800000),
    (df_limpio["ANNUAL INCOME"]> 800000) & (df_limpio["ANNUAL INCOME"]<= 900000),
    (df_limpio["ANNUAL INCOME"]> 900000) & (df_limpio["ANNUAL INCOME"]<= 1000000),
    (df_limpio["ANNUAL INCOME"]> 1000000) & (df_limpio["ANNUAL INCOME"]<= 1500000),
    (df_limpio["ANNUAL INCOME"]> 1500000) & (df_limpio["ANNUAL INCOME"]<= 2000000)
    ]

values = ("1","2","3","4","5","6","7","8","9","10","11","12")
df_limpio["ANNUAL INCOME"]= np.select(conditions,values)
df_limpio["ANNUAL INCOME"].value_counts().sort_index()

#Hacemos variable int
df_limpio["ANNUAL INCOME"]= df_limpio["ANNUAL INCOME"].astype(int)

#Hacemos variable int
df_limpio["ACCOUNT STATUS"]= df_limpio["ACCOUNT STATUS"].astype(int)

#Corroboramos types
df_limpio.info()

#Transformamos las variables categóricas en numéricas
df_limpio = pd.get_dummies(df_limpio)
df_limpio

#Vemos las nuevas columnas y su info
df_limpio.info()

df_limpio.value_counts("ANNUAL INCOME").sort_index()

len(df_limpio)

type(df_limpio)

#Grafico de barras de ACCOUNT STATUS
df_limpio["ACCOUNT STATUS"].value_counts().plot.bar()

#0: 1-29 días de atraso 
#1: 30-59 días de atraso 
#2: 60-89 días de atraso  
#3: 90-119 días de atraso 
#4: 120-149 días de atraso 
#5: Deudas atrasadas o incobrables,canceladas por más de 150 días
#6: pagado ese mes 
#7: No hay préstamo para el mes

#La categoria que predomina es la 6, es decir, pago ese mes. La segunda es la 0, es decir, 1-29 días de retraso

df_limpio["ACCOUNT STATUS"].value_counts()

df_limpio["ANNUAL INCOME"].describe().round()

#Grafico de ANNUAL INCOME
df_limpio["ANNUAL INCOME"].value_counts().sort_index().plot.line()
#Predominan los salarios entre $100K y $300K

#Expresado en gráfico de barrras
sns.countplot(df_limpio["ANNUAL INCOME"])

#Expresado en boxplot
sns.boxplot(df_limpio["ANNUAL INCOME"], orient="V")

df_limpio["ANNUAL INCOME"].value_counts()

#boxplot de mes de balance
sns.boxplot(df_limpio["MONTHS OF BALANCE"], orient="V")

frec = df_limpio['EDUCATION LEVEL_Higher education'].value_counts()
frec

frec.sum()

frec_df = pd.DataFrame(frec)
frec_df

frec_df.rename(columns={"EDUCATION LEVEL_Higher education":"FREC ABS"},inplace=True)
frec_df

frec_abs_values = frec_df["FREC ABS"].values
acum = [] #esto es una lista vacia donde pondremos frec abs acumuladas
valor_acum = 0
for i in frec_abs_values:
  valor_acum = valor_acum + i
  acum.append(valor_acum)
frec_df["FREC ABS ACUM"] = acum
frec_df

frec_df["FREC RELATIVA"] = round(100 * frec_df["FREC ABS"] / len(df_limpio["EDUCATION LEVEL_Higher education"]), 4)
frec_df

frec_rel_values = frec_df["FREC RELATIVA"].values
acum = []
valor_acum = 0
for i in frec_rel_values:
  valor_acum = valor_acum + i
  acum.append(valor_acum)
frec_df["FREC RELATIVA ACUM"]=acum
frec_df

#Vemos la relación entre variables
plt.figure(figsize=(40, 30))

vg_corr = df_limpio.corr()
sns.heatmap(vg_corr, 
            xticklabels = vg_corr.columns.values,
            yticklabels = vg_corr.columns.values,
            annot = True);

#Creamos un sub-dataframe sobre educación 
academic = df_limpio["EDUCATION LEVEL_Academic degree"].value_counts()
academic2= df_limpio["EDUCATION LEVEL_Higher education"].value_counts()
academic3 = df_limpio["EDUCATION LEVEL_Incomplete higher"].value_counts()
academic4 = df_limpio["EDUCATION LEVEL_Lower secondary"].value_counts()
academic5= df_limpio["EDUCATION LEVEL_Secondary / secondary special"].value_counts()
df_education = pd.DataFrame([academic,academic2,academic3,academic4,academic5])
df_education

df_education.dtypes

#Vemos como se comporta cada variable
df_education.plot.bar()

#Relacionamos EDUCATION con ANNUAL INCOME
sns.barplot(df_limpio["ANNUAL INCOME"], df_limpio['EDUCATION LEVEL_Secondary / secondary special'])

#Relacionamos EDUCATION con ANNUAL INCOME
sns.barplot(df_limpio['ACCOUNT STATUS'], df_limpio['EDUCATION LEVEL_Secondary / secondary special'])

pd.crosstab(df_limpio["ACCOUNT STATUS"], df_limpio["INCOME CATEGORY_Working"])

pd.crosstab(df_limpio["ACCOUNT STATUS"], df_limpio["ANNUAL INCOME"])

plt.figure(figsize=(10,10))
plt.rcParams['figure.figsize'] = (12, 9)
sns.boxplot(df_limpio['ACCOUNT STATUS'], df_limpio['ANNUAL INCOME'], palette = 'viridis')
plt.show()

#MONTHS_BALANCE significa de que mes es el resumen de cuenta. 0 es el mes actual, -1 es el mes anterior, etc.
#STATUS significa si status de la cuenta y del pago.Significados:
  #0: 1-29 días de atraso 
  #1: 30-59 días de atraso 
  #2: 60-89 días de atraso  
  #3: 90-119 días de atraso 
  #4: 120-149 días de atraso 
  #5: Deudas atrasadas o incobrables,canceladas por más de 150 días
  #6: pagado ese mes 
  #7: No hay préstamo para el mes

plt.figure(figsize=(10,10))
plt.rcParams['figure.figsize'] = (12, 9)
sns.boxplot(df_limpio['CHILDREN'], df_limpio['BIRTHDAY'], palette = 'viridis')
plt.show()

sns.FacetGrid(df, hue="MARITAL STATUS", size= 5).map(plt.scatter,"FAMILY SIZE", "CHILDREN").add_legend();
plt.show

sns.FacetGrid(df, hue="GENDER", size= 5).map(plt.scatter,"ACCOUNT STATUS", "INCOME CATEGORY").add_legend();
plt.show