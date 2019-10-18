import urllib.request, json, http.client, urllib.parse, urllib.error, bs4, time, datetime, requests

bus = '13'
fermata = '2017'
orario_input = '09:50'
direzione = '1'
date = datetime.datetime.now()
tabellaorari='https://m.atv.verona.it/api/datetime/{}-{}-{}-00-00/routes/{}/d/{}/stops/{}/stoptimes'.format(date.year,date.month,date.day,bus,direzione,fermata)
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

for i in json_orari:
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
        y='<font color="#ff0000">+{}</font> 9:{}'.format(int(i[5])//60,int(i[5])//60+50)
      if int(i[5])//60 <= 0:
        y='<font color="#00c200">{}</font> 9:{}'.format(int(i[5])//60,int(i[5])//60+50)  
      print('bus: {} - direzione: {} - id_viaggio: {} - ultima fermata: {} - fermate fatte: {} - ritardo: {} min - bho1: {} - bho2: {} - bho3: {}'.format(i[0],i[1],i[2],i[3],i[4],int(i[5])//60,i[6],i[7],i[8]))
      conn = http.client.HTTPSConnection("api.pushover.net:443")
      conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
          "token": "token",
          "user": "user",
          "message": y,
          "priority": "0",
          "html": "1",
          "title": "13",
        }), { "Content-type": "application/x-www-form-urlencoded" })
      conn.getresponse()
      z=i[5]
      if time.time() > start + periodtime: 
        break
      
     

