
import bs4
import json
import urllib.request
webpage=str(urllib.request.urlopen("https://m.atv.verona.it/api/realtime/updates/routes/90%7C13").read())
soup = bs4.BeautifulSoup(webpage,features="html.parser")
txt = soup.get_text()
txt = txt.replace("b'","[")
txt = txt.replace("]'","]]")
txt = txt.replace('","','"],["')
txt = txt.replace("|",'","')
orario = json.loads(txt)
for i in orario:
  print('bus: {} - direzione: {} - id_viaggio: {} - ultima fermata: {} - fermate fatte: {} - ritardo: {} sec - bho1: {} - bho2: {} - bho3: {}'.format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))




#sabato 13 6:48 numero corsa: 386_1325598
