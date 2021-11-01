import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import pywikibot

clubID = 'Q18656'

endpoint_url = "https://query.wikidata.org/sparql"
entities = ['inception', 'founders', 'chair', 'country', 'coach', 'stadium', 'owners', 'sponsor', 'league', 'where', 'colors', 'capacity']
query = """SELECT ?inception ?founders ?chair ?country ?coach ?stadium ?owners ?sponsor ?league ?where ?colors ?capacity
WHERE
{
  wd:""" + clubID + """ wdt:P571 ?inception;
            wdt:P112 ?founders;
            wdt:P488 ?chair;
            wdt:P17 ?country;
            wdt:P286 ?coach;
            wdt:P115 ?stadium;
            wdt:P127 ?owners;
            wdt:P859 ?sponsor;
            wdt:P118 ?league;
            wdt:P159 ?where;
            wdt:P6364 ?colors.
  ?stadium wdt:P1083 ?capacity.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
}"""
storage = {}
for i in entities:
  storage[i] = set()

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
  for j in result:
    temp = result[j]['value']
    value = temp.split('/')[-1]
    if j != 'inception' and j != 'capacity':
      site = pywikibot.Site("wikidata", "wikidata")
      repo = site.data_repository()
      item = pywikibot.ItemPage(repo, value)
      item_dict = item.get()
      if 'hi' in item_dict['labels']:
        value = item_dict['labels']['hi']
      else:
        value = item_dict['labels']['en']
    storage[j].add(value)

for i in storage:
  if len(storage[i]) > 1:
    temp = list(storage[i])
    newStr = temp[0]
    for j in temp[1:]:
      newStr += ', ' + j
    storage[i] = str(newStr)
  else:
    for jk in storage[i]:
      storage[i] = str(jk)

print(storage)

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, clubID)
item_dict = item.get()
storage['name'] = item_dict['labels']['hi']

sentences = []
sentences.append(storage['name'] + ' एक प्रसिद्ध फुटबॉल क्लब है।')
sentences.append('यह ' + storage['where'] + ' में स्थित है।')
sentences.append('इसकी स्थापना ' + storage['inception'] + ' में ' + storage['founders'] + ' द्वारा की गई थी।')
sentences.append('यह वर्तमान में ' + storage['owners'] +' के स्वामित्व में है।')
sentences.append('यह ' + storage['stadium'] + ' में अपने घरेलू खेल खेलता है।')
sentences.append('इस स्टेडियम में अधिकतम ' + storage['capacity'] + ' लोग बैठ सकते हैं।')
sentences.append(storage['name'] + ' अभी ' + storage['league'] + ' में खेलता है।')
sentences.append('यह ' + storage['coach'] + ' द्वारा प्रशिक्षित है।')
sentences.append('इसकी आधिकारिक जर्सी में ' + storage['colors'] + ' रंग होते हैं।')
sentences.append('अन्य सभी क्लबों की तरह, इस क्लब को ' + storage['sponsor'] + ' से भारी प्रायोजन मिलते हैं।')
print(sentences)