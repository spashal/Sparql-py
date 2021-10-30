import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import pywikibot

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?child ?childLabel
WHERE
{
# ?child  father   Bach
  ?child wdt:P22 wd:Q1339.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
}"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result)

    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()

    # iD = result['childLabel']['value']
    # iD = iD.split('/')
    # item = pywikibot.ItemPage(repo, result['childLabel']['value'])
    item = pywikibot.ItemPage(repo, 'Q11571')
    item_dict = item.get()
    print(item_dict["labels"]['hi'])
    break
    for clm in clm_list:
        clm_trgt = clm.getTarget()
        print(clm_trgt.amount)
        print(clm_trgt.unit)
# print(results)