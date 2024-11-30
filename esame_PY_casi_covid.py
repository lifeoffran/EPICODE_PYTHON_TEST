import pandas as pd
import math
import seaborn as sns
import matplotlib.pyplot as plt

#Apro il DataFrame
fileName = "owid-covid-data.csv" 
data = pd.read_csv(fileName, usecols=['location', 'date', 'total_cases', 'new_cases', 'icu_patients', 'weekly_hosp_admissions'])

# 1. Verifica delle dimensioni del dataset
print("Dimensioni del dataset (righe, colonne):", data.shape,'\n')

# 2. Visualizza i metadati (nomi colonne e tipi di dati)
print("\nMetadati del dataset:",'\n')
print(data.dtypes)

#3_1. Numero casi totali per continente dall'inizio della pandemia

lista_continenti = {'Africa': 0, 'Europe': 0, 'Asia': 0, 'Oceania': 0, 'North America': 0, 'South America': 0}

#Sommo i nuovi casi per ogni continente
for dato in data.values:
    if dato[0] == 'Africa' and not math.isnan(dato[3]):
        lista_continenti['Africa'] = lista_continenti['Africa']+int(dato[3])
    if dato[0] == 'Europe' and not math.isnan(dato[3]):
        lista_continenti['Europe'] = lista_continenti['Europe']+int(dato[3])
    if dato[0] == 'Asia' and not math.isnan(dato[3]):
        lista_continenti['Asia'] = lista_continenti['Asia']+int(dato[3])
    if dato[0] == 'Oceania' and not math.isnan(dato[3]):
        lista_continenti['Oceania'] = lista_continenti['Oceania']+int(dato[3])
    if dato[0] == 'North America' and not math.isnan(dato[3]):
        lista_continenti['North America'] = lista_continenti['North America']+int(dato[3])
    if dato[0] == 'South America' and not math.isnan(dato[3]):
        lista_continenti['South America'] = lista_continenti['South America']+int(dato[3])

print(
    '\n\nNumero casi totali per continente dall\'inizio della pandemia:\n'
    'Africa: ', lista_continenti['Africa'],'\n'
    'Europa: ', lista_continenti['Europe'], '\n'
    'Asia: ', lista_continenti['Asia'], '\n'
    'Oceania: ', lista_continenti['Oceania'], '\n'
    'America del Nord: ', lista_continenti['North America'], '\n'
    'America del Sud: ', lista_continenti['South America'],'\n'
)

#3_2. Percentuale per continente rispetto al totale mondiale

somma_mondiale = lista_continenti['Africa']+lista_continenti['Asia']+lista_continenti['Europe']+lista_continenti['North America']+lista_continenti['South America']+lista_continenti['Oceania']

#Calcolo le percentuali per ogni continente
percentuale_Continente = {
    'Africa': round(lista_continenti['Africa']/somma_mondiale*100, 2),
    'Europe': round(lista_continenti['Europe']/somma_mondiale*100, 2),
    'Asia': round(lista_continenti['Asia']/somma_mondiale*100, 2),
    'Oceania': round(lista_continenti['Oceania']/somma_mondiale*100, 2),
    'North America': round(lista_continenti['North America']/somma_mondiale*100, 2),
    'South America': round(lista_continenti['South America']/somma_mondiale*100, 2)
}

print(
    '\n\nPercentuale per continente rispetto al totale mondiale:\n'
    'Africa: ', percentuale_Continente['Africa'],'%\n'
    'Europa: ', percentuale_Continente['Europe'], '%\n'
    'Asia: ', percentuale_Continente['Asia'], '%\n'
    'Oceania: ', percentuale_Continente['Oceania'], '%\n'
    'America del Nord: ', percentuale_Continente['North America'], '%\n'
    'America del Sud: ', percentuale_Continente['South America'],'%\n'
)


#4 Filtra i dati per l'Italia nel 2022
italy_data = data[(data['location'] == 'Italy') & 
                  (data['date'] >= '2022-01-01') & 
                  (data['date'] <= '2022-12-31')]

# Converte la colonna 'date' in formato datetime
italy_data['date'] = pd.to_datetime(italy_data['date'])

# Imposta lo stile predefinito di Seaborn
sns.set_theme(style="whitegrid")

#Grafico dei casi totali
plt.figure(figsize=(12, 6))
sns.lineplot(data=italy_data, x='date', y='total_cases', label='Casi Totali', color='blue')
plt.title('Evoluzione dei Casi Totali in Italia (2022)', fontsize=16)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Casi Totali', fontsize=12)
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Controlla i dati mancanti in 'new_cases'
missing_new_cases = italy_data['new_cases'].isnull().sum()
print(f"Valori mancanti in 'new_cases': {missing_new_cases}")

# Controllo se new_cases ha dati validi, altrimenti passo a new_cases_smoothed
if italy_data['new_cases'].notnull().sum() > 0:
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=italy_data, x='date', y='new_cases', label='Nuovi Casi', color='orange')
    plt.title('Nuovi Casi Registrati in Italia (2022)', fontsize=16)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Nuovi Casi', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()
else:
    print("I dati di 'new_cases' non sono disponibili. Utilizzo 'new_cases_smoothed'.")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=italy_data, x='date', y='new_cases_smoothed', label='Nuovi Casi (Smoothed)', color='green')
    plt.title('Nuovi Casi (Media Settimanale) Registrati in Italia (2022)', fontsize=16)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Nuovi Casi (Smoothed)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

# Filtra i dati per Italia, Germania e Francia e per il periodo maggio 2022 - aprile 2023
stati_selezionati = ['Italy', 'Germany', 'France']
filtered_data = data[(data['location'].isin(stati_selezionati)) & 
                     (data['date'] >= '2022-05-01') & 
                     (data['date'] <= '2023-04-30')]

# Rimuovi valori mancanti in 'icu_patients'
filtered_data = filtered_data[filtered_data['icu_patients'].notnull()]

# Creazione del boxplot
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")
sns.boxplot(data=filtered_data, x='location', y='icu_patients', palette="Set2")
plt.title('Confronto tra i pazienti in terapia intensiva (Maggio 2022 - Aprile 2023)', fontsize=16)
plt.xlabel('Nazione', fontsize=12)
plt.ylabel('Pazienti in Terapia Intensiva (ICU)', fontsize=12)
plt.show()

#Il boxplot confronta il numero di pazienti in terapia intensiva nel periodo maggio 2022 - aprile 2023 (ICU) tra 
# Francia, 
# Germania
# Italia
# La Germania presenta il carico maggiore, con alta variabilità e una mediana elevata. 
# La Francia segue con valori più contenuti e moderata variabilità. 
# L'Italia mostra i numeri più bassi, con scarsa variabilità, indicando un impatto ridotto rispetto agli altri paesi. 
# Differenze dovute a capacità ospedaliera, strategie sanitarie o demografia.

#5 Filtra le nazioni richieste e il periodo 2023
stati_selezionati = ['Italy', 'Germany', 'France', 'Spain']
data_filtrati = data[(data['location'].isin(stati_selezionati)) & 
                     (data['date'] >= '2023-01-01') & 
                     (data['date'] <= '2023-12-31')]

#Calcolo della somma per ciascun paese
summary = data_filtrati.groupby('location')['weekly_hosp_admissions'].sum()

# Controllo dei dati nulli
missing_data = data_filtrati['weekly_hosp_admissions'].isnull().sum()
print("Dati mancanti nella colonna 'weekly_hosp_admissions':", missing_data)

# Mostra la somma dei pazienti ospitalizzati per ogni nazione
print("\nSomma dei pazienti ospitalizzati nel 2023:")
print("Francia: ", int(summary.iloc[0]))
print("Germania: ", int(summary.iloc[1]))
print("Italia: ", int(summary.iloc[2]))
print("Spagna: ", int(summary.iloc[3]))


#È possibile gestire i dati nulli sostituendoli con il valore medio dei dati di quella colonna