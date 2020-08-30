from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

def auth_with_gsheet():
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Path/to/credentials.json', scope)
    return gspread.authorize(credentials)

@app.route('/')
def index():
    client = auth_with_gsheet()
    sheet = client.open('Name_of_Workbook').worksheet('Name_of_Worksheet')
    data = sheet.get_all_values()
    for i in range(len(data)):
        if i == 0:
            continue
        else:
            data[i][3] = float(data[i][3].replace('$','').replace(',',''))
            data[i][4] = int(data[i][4])
            data[i][5] = float(data[i][5].replace('$','').replace(',',''))
            data[i].append(round(data[i][4]*data[i][5],2))
            data[i].append(float(data[i][7].replace('%','').replace(',','')))
            data[i].append(round(data[i][8] - data[i][3]*data[i][4],2))
    return render_template('index.html', data=data[1:])