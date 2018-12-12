import requests
jsond = {
    'main': "main.tex",
    'session':'cXfRZUqW4TpCrvzLR1NkVgoRhP9os9Dg',
    'resources': [
        {
            'name':'main.tex',
            'url':'https://www3.nd.edu/~powers/ame.20231/sample.tex',
            'modified_time':1300,
        },

    ],
    'mode': 'simple'
}
r = requests.post('http://127.0.0.1:5000/compiler', json=jsond)
print(r.text)