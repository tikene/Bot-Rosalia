from google.oauth2 import service_account
from gdoctableapppy import gdoctableapp
import os


document_id = "1h_Cs5HAdyIxtXZ5ldXbb1WjgB1zDJLtvgT-2r3aA4_0"
string_hora = "hora"


SCOPES = ['https://www.googleapis.com/auth/documents']
#SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), "Telegram_Bot", "service_account.json")
SERVICE_ACCOUNT_FILE = "service_account.json"
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


resource = {
    "oauth2": creds,
    "documentId": document_id,
    # "showAPIResponse": True
}


def getDriveTable(lastversion=False):


    dias = { 'LUNS': {}, 'MARTES':{}, 'MÉRCORES':{}, 'XOVES':{}, 'VENRES':{} }


    tablaHorarios = gdoctableapp.GetTables(resource) # You can see the retrieved values like this.

    versionTabla = tablaHorarios["libraryVersion"]

    if lastversion and (versionTabla == lastversion):

        return False, False    # La tabla no ha cambiado


    # AÑADIR HORAS A CADA DIA

    for i in tablaHorarios["tables"][0]["values"]:

        valor = i[0]

        if (valor.lower() == string_hora) or (valor == ""):

            continue

        else:

            for i in dias:

                dias[i][valor] = {}

    # AÑADIR CLASES A CADA HORA DENTRO DE CADA DIA

    for i in range(1, len(tablaHorarios["tables"][0]["values"])):

        columna_vertical = tablaHorarios["tables"][0]["values"][i]

        hora = columna_vertical[0]

        if hora == "":
            continue

        #clase_lunes = columna_vertical[1].rstrip()
        #clase_martes = columna_vertical[2].rstrip()
        #clase_miercoles = columna_vertical[3].rstrip()
        #clase_jueves = columna_vertical[4].rstrip()
        #clase_viernes = columna_vertical[5].rstrip()


        for dia in dias:

            pos_dia = tuple(dias).index(dia) + 1

            dias[dia][hora] = columna_vertical[pos_dia].rstrip()



    return versionTabla, dias
