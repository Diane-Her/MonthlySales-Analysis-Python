# %% [markdown]
# ### Data Analysis
# **Data cleaning, formatting, transformation and visualization.**
# 
# Autor: DianaHer 

# %% [markdown]
# **Script reutilizable para el análisis mensual de ventas**
# 
# *Este análisis ha sido diseñado para ser reutilizado cada mes, con la premisa de recibir un resumen de ventas periódicamente. Su objetivo es identificar fortalezas y áreas de oportunidad en tres aspectos clave: productos, regiones de venta y desempeño del equipo de ventas.*

# %%
# PASO 01. Instalación de paquetes

import pandas as pd
import seaborn as sns
import numpy as nmp
import matplotlib as mpl

# %%
# PASO 02. Importación de archivos.
# Realizar una visualización previa del archivo csv para corregir potenciales errores de importación.

df_sellers = pd.read_csv("C:\\Users\\Usuario\\OneDrive\\Documentos\\Python\\Curso Udemy Análisis de Datos con Pandas y Python\\datasets\\ventasTotales.csv", sep = ';', skiprows = 5)   

# %%
# PASO 03. Revisión y limpieza de datos.

df_sellers.head()


# %%
df_sellers.info()

# %% [markdown]
# *El dataset cuenta con 7 columnas con información de las ventas por región, categoría, ganancias, entre otras. Y cuenta con 460 registros.*

# %%
# Limpieza del dataset.
# Quitar espacios en blanco, convertir a minúsculas, quitar acentos y caracteres fuera del codigo ASCII

df_sellers.columns = (
    df_sellers.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.normalize('NFKD')
    .str.encode('ascii', errors = 'ignore').str.decode('utf-8'))

df_sellers.head()

# %%
# Verificar si existen registros duplicados

duplicated = df_sellers[df_sellers.duplicated()]
print(duplicated)

# %%
# Eliminar registros duplicados

df_sellers_clean = df_sellers.drop_duplicates()
df_sellers_clean.info() # Revisar que el valor ya fue eliminado

# %%
# PASO 04. Realizar cálculos para el análisis de datos.
# Verificar los artículos más vendidos.

df_sc = df_sellers_clean
df_sc.articulo.value_counts()

# %% [markdown]
# *En la previa lista se puede observar el número de ventas por artículo, es fácil apreciar los tres artículos más vendidos: escoba(31), bufanda(28) y pan(26).*

# %%
# Reemplazar las comas por puntos para poder converitr la columna de ganancia a valor numérico

df_sc['ganancia'] = df_sc['ganancia'].str.replace(',', '.')
df_sc.head()

# %%
# Cambiar el formato de la columna ganancia

df_sc['ganancia'] = pd.to_numeric(df_sc['ganancia'])
df_sc.info()

# %%
df_sc.info()

# %%
# Verificar que artículo genera más ganancia

totales_artículos = df_sc.groupby('articulo')['ganancia'].sum()

totales_artículos = totales_artículos.sort_values(ascending = False)

# Convertirlo a df haciendo reset del índice

totales_artículos = totales_artículos.reset_index()
totales_artículos

# %%
# Seleccionar solo los 5 artículos con mayores ganancias

top5_artículos = totales_artículos.head(5)
top5_artículos

# %%
# Realizar un gráfico representativo para los primeros tres artículos, así como para el total de las ganancias por artículo.

#Instalar pypilot para mejor manejo de los atributos del gráfico

import matplotlib.pyplot as plt

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(6, 5))

# Definir tipo y componentes del gráfico
ax.bar(top5_artículos['articulo'], top5_artículos['ganancia'])

# Añadir etiquetas de valor en la cima de cada barra
for i, valor in enumerate(top5_artículos['ganancia']):
    ax.text(i, valor, f'{valor:.2f}', ha='center', va='bottom')  # Formato con 2 decimales

# Personalizar etiquetas y título
ax.set_xlabel('Artículo')
ax.set_ylabel('Ganancia Total')
ax.set_title('Artículo con más Ganancias')
ax.set_xticklabels(top5_artículos['articulo'], rotation=90)
ax.bar(top5_artículos['articulo'], top5_artículos['ganancia'], color='mediumseagreen')

 #Ajustar y mostrar gráfico
plt.tight_layout()  
plt.show()

# %% [markdown]
# *Podemos observar como es que los artículos que más se venden, no son necesariamente los que generan más ganancia, debido al precio unitario por artículo los que generan mayor ganancia son: sandalias, sudadera y escoba*

# %%
# Determinar el total de ganancias según la categoría
totales_categoria = df_sc.groupby('categoria')['ganancia'].sum()

totales_categoria = totales_categoria.sort_values(ascending = False)

totales_categoria = totales_categoria.reset_index()

totales_categoria


# %%
# Realizar un gráfico circular representativo

# Crear el gráfico circular
plt.figure(figsize=(5,5))

# Personalizar atributos del gráfico
plt.pie(totales_categoria['ganancia'], labels=totales_categoria['categoria'], autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightskyblue', 'palegreen'])
plt.title('Distribución de Ganancia por Categoría')

# Ajustar y mostrar
plt.tight_layout()
plt.show()


# %%
# Mostrar solo los valores de ventas totales para cada vendedor

totales_vendedor = df_sc.groupby('vendedor')['ganancia'].sum()

totales_vendedor = totales_vendedor.sort_values(ascending = False)

totales_vendedor = totales_vendedor.reset_index()
totales_vendedor



# %%
#Crear gráfico representativo con el vendedor que ha generado más ganancias en el mes

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(6, 5))

# Definir tipo y componentes del gráfico
ax.bar(totales_vendedor['vendedor'], totales_vendedor['ganancia'])

# Añadir etiquetas de valor en la cima de cada barra
for i, valor in enumerate(totales_vendedor['ganancia']):
    ax.text(i, valor, f'{valor:.2f}', ha='center', va='bottom')  # Formato con 2 decimales

# Ajustar etiquetas y título
ax.set_xlabel('Vendedor')
ax.set_ylabel('Ganancia Total')
ax.set_title('Ganancia Mensual por Vendedor')
ax.set_xticklabels(totales_vendedor['vendedor'], rotation=90)
ax.bar(totales_vendedor['vendedor'], totales_vendedor['ganancia'], color='lightseagreen')

# Ajustar y mostrar el gráfico
plt.tight_layout()  
plt.show()

# %% [markdown]
# *El vendedor con mayor ganancia en ventas del mes es Dustin Gee, mientras que el vendedor con menor ganancia es Sarah Bond.*

# %%
# Calcular en que región se generan más ganancias

ventas_región = df_sc.groupby('region')['ganancia'].sum()
ventas_región.sort_values(ascending = False)
ventas_región = ventas_región.reset_index()
ventas_región


# %%
# Realizar un gráfico circular para visualizar los porcentajes de ventas

plt.figure(figsize=(5,5))

plt.pie(ventas_región['ganancia'], labels=ventas_región['region'], autopct='%1.1f%%', startangle=90, colors= ['lightcoral', 'lightskyblue', 'palegreen', 'lightgoldenrodyellow'])
plt.title('Distribución de Ganancia por Región')

plt.tight_layout()
plt.show()

# %% [markdown]
# *Podemos observar como la distribución de las ganancias no representa valores mayores o menores extremos para ninguna de las regiones. Sin embargo las ganancias son ligeramente mayores en la región del Este con un 29.2% en total*

# %% [markdown]
# <div class="alert alert-info">
# <b>Nota:</b> Reemplazar el archivo .csv para realizar el próximo análisis de ventas mensual.
# </div>
# 

# %% [markdown]
# 


