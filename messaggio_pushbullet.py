import urllib.request, json, http.client, urllib.parse, urllib.error, bs4, time, datetime, requests
from pushbullet import Pushbullet

pb = Pushbullet("token")
bus = '13'
fermata = '2017'
orario_input = '9:50'
direzione = '1'
date = datetime.datetime.now()
giorno=date.strftime("%d")
tabellaorari='https://m.atv.verona.it/api/datetime/{}-{}-{}-00-00/routes/{}/d/{}/stops/{}/stoptimes'.format(date.year,date.month,giorno,bus,direzione,fermata)
live = 'https://m.atv.verona.it/api/realtime/updates/routes/{}'.format(bus)
x=0
z=99999999
secondi=["%.2d" % i for i in range(60)]
start = time.time()
periodtime = 1000
print(live)
print(tabellaorari)

json_orari = json.loads(requests.get(tabellaorari).text)

for i in json_orari:
  for count in secondi:
    orario = "{}:{}".format(orario_input,count)
    if  i['departureTimeChar'] == orario:
      print('codice: {}'.format(i['tripID']))
      codice = i['tripID']

while True:
  time.sleep(5)
  webpage=str(urllib.request.urlopen(live).read())
  soup = bs4.BeautifulSoup(webpage,features="html.parser")
  txt = soup.get_text()
  txt = txt.replace("b'","[")
  txt = txt.replace("]'","]]")
  txt = txt.replace('","','"],["')
  txt = txt.replace("|",'","')
  orarilive = json.loads(txt)
  if time.time() > start + periodtime: 
    break
  for i in orarilive:
    if  i[2] == codice:
      x=x+1
      if z == i[5]:
        print("check {}".format(x))
        break
      if int(i[5])//60 > 0:
        y="+{} 13:{}".format(int(i[5])//60,int(i[5])//60+50)
      if int(i[5])//60 <= 0:
        y="{} 13:{}".format(int(i[5])//60,int(i[5])//60+50)  
      print('bus: {} - direzione: {} - id_viaggio: {} - ultima fermata: {} - fermate fatte: {} - ritardo: {} min - bho1: {} - bho2: {} - bho3: {}'.format(i[0],i[1],i[2],i[3],i[4],int(i[5])//60,i[6],i[7],i[8]))
      push = pb.push_note("13", y)
      z=i[5]
      if time.time() > start + periodtime: 
        break
