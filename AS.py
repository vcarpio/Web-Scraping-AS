from bs4 import BeautifulSoup
import requests
import pandas as pd


url = 'https://resultados.as.com/resultados/futbol/primera/clasificacion/'
pagina = requests.get(url)

#soup contendrá el objeto BeautifulSoup que representa la estructura del documento HTML y
# se puede utilizar para navegar y extraer información del contenido HTML de pagina.content
soup = BeautifulSoup(pagina.content, 'html.parser')

#Equipos
#El resultado de esta línea de código será una lista de todos los elementos <span> que tienen la clase CSS nombre-equipo.
# Cada elemento de la lista representará un equipo encontrado en el documento HTML analizado por BeautifulSoup
team= soup.find_all('span',class_ = 'nombre-equipo')

equipos = []
aux = 0
for equipo in team:
    if aux < 20:
        equipos.append(equipo.text)
    else:
        break
    aux += 1

#Puntos
points = soup.find_all('td',class_ = 'destacado')
puntos = []
#Partidos
partidos = soup.find('table', class_='tabla-datos table-hover').find_all('tr')

jugados = []
ganados = []
empatados = []
perdidos = []

aux=0
for i in points:
    if aux < 20:

        puntos.append(i.text)
        pjugados = i.find_next_sibling('td')
        jugados.append(pjugados.text)
        pganados = pjugados.find_next_sibling('td')
        ganados.append(pganados.text)
        pempatados = pganados.find_next_sibling('td')
        empatados.append(pempatados.text)
        pperdidos = pempatados.find_next_sibling('td')
        perdidos.append(pperdidos.text)

    else:
        break
    aux += 1

#lo meto todo en un dataframe

df = pd.DataFrame({'Nombre': equipos, 'Puntos': puntos, 'P.Jugados': jugados, 'P.Ganados': ganados, 'P.Empatados': empatados, 'P.Perdidos': perdidos}, index=list(range(1,21)))

#index=False evita que pandas incluya el índice del DataFrame como una columna adicional en el archivo CSV.
df.to_csv('Clasificación.csv', index = False)
print(df)
