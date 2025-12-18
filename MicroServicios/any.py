topics = [

  {

        'id': 1,

        'title': "Node.js Basico",

        'votes': 10,

        'links': [

            { 'id': 101, 'url': "https://nodejs.org", 'description': "Doc Oficial"}
        ]
    }
]



claves_dic = topics[0].keys()

for a in claves_dic:
    if a == 'links':
        get_url = topics[0].get(a)
        print(get_url[0].get('url'))