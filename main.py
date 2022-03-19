import re
import PyPDF2
import pandas as pd


"""

"""

# Setting the file path
pdf_path = 'ED_8_PETROBRAS_PSP1_2021_RES_FINAL_OBJ_CONV_TITULOS.PDF'

# Reading the PDF file with PyPDF2
with open(pdf_path, mode='rb') as f:
    reader = PyPDF2.PdfFileReader(f)
    # Getting the number of pages
    num_pages = reader.getNumPages()
    # Getting the document content
    pdf_content = ''
    for i in range(num_pages):
        page = reader.getPage(i)
        # Getting the page content
        text = page.extractText().replace('\n', '')
        # Removing the page number and adding it to the full content
        pdf_content += text[text.find(str(i + 1)) + len(str(i + 1)):]

# Configuring regular expression to find titles
pattern = r'ÊNFASE \d{1,2}([^a-z\d])+'
matches = re.finditer(pattern, pdf_content)

enfases = []
# Getting the name and position of titles
for match in matches:
    i1 = match.start()
    i2 = match.end()
    name = match.group()
    if name[-2:] == ' R':
        name = name[:-2]

    enfase = {
        'name': name.strip(),
        'position': (i1, i2)
    }
    enfases.append(enfase)

n_enfases = len(enfases)

# Preparing the dataframe
columns_resultados = ['Ênfase', 'Nº de inscrição', 'Nome do candidato', 'Nota final - Conhecimentos básicos',
                      'Nº acertos - Conhecimentos básicos', 'Nota final - Conhecimentos específicos',
                      'Nº acertos - Conhecimentos específicos', 'Nota final - Bloco 1', 'Nota final - Bloco 2',
                      'Nota final - Bloco 3', 'Nota final da prova']
df_enfases = []
for idx, enfase in enumerate(enfases):
    # Getting the content between titles to assign it to the top one
    i1 = enfase['position'][1]
    i2 = enfases[idx + 1]['position'][0] if idx != (n_enfases - 1) else -1
    content = pdf_content[i1:i2]

    # Configuring regular expression to find candidate result information
    pattern = r'\d{8}([^/])+'
    candidates = [candidate.group() for candidate in re.finditer(pattern, content)]

    candidates_rows = []
    for candidate in candidates:
        # Breaking the string and configuring the candidate row
        column_data = candidate.split(',')
        insc = int(column_data[0])
        name = column_data[1].strip()
        nf1 = float(column_data[2])
        a1 = int(column_data[3])
        nf2 = float(column_data[4])
        a2 = int(column_data[5])
        bl1 = float(column_data[6])
        bl2 = float(column_data[7])
        bl3 = float(column_data[8])
        # Getting the final result through regex because the end of last element doesn't always end in the score
        nf = float(re.search(r'\d{1,2}\.\d{2}', column_data[9]).group())
        candidates_rows.append([enfase['name'], insc, name, nf1, a1, nf2, a2, bl1, bl2, bl3, nf])

    # Creating the dataframe with the candidate results for the current enfase
    df_enfase = pd.DataFrame(columns=columns_resultados, data=candidates_rows)
    df_enfases.append(df_enfase)

# Merging all dataframes into one
df_final = pd.concat(df_enfases)

# Saving the dataframe to a csv file
df_final.to_csv('aprovados_petrobras_2022.csv', index=False)
