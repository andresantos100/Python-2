import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

dados_conceitos = {#dicionario com as informações da caixa dopdown 
                                #- jason com varios campos
'java' : {'variaveis':8, 'condicionais':10, 'loops': 4, 'poo': 3, 'funcoes':4 }
'python' : {'variaveis':9, 'condicionais':7, 'loops': 8, 'poo': 4, 'funcoes':5 }
'sql' : {'variaveis':7, 'condicionais':10, 'loops': 9, 'poo': 4, 'funcoes':4 }
'golang' : {'variaveis':10, 'condicionais':5, 'loops': 8, 'poo': 3, 'funcoes':3 }
'javascript' : {'variaveis':8, 'condicionais':7, 'loops': 7, 'poo': 3, 'funcoes':8 }
}

cores_map = dict(
    java = 'red',
    python = 'green',
    sql='yellow',
    golang='blue',
    javascript='pink'
)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H4(
        'Sebrae Maranhão',
        style={'textAlign':'center'}
    ),
     html.Div(
         dcc.Dropdown(#menu dropdown
             id="dropdown_linguagens",
             options=[
                {'label':'Java','valor':'java'}
                {'label':'Python','valor':'python'}
                {'label':'SQL','valor':'sql'}
                {'label':'GoLang','valor':'golang'}
                {'label':'JavaScript','valor':'javascript'}
             ],
             value=['java'],
             multi=True,
             style={'width': '50%','margin':'0 auto'}
         )
    ),
    dcc.Graph(id='grafico_Linguagens')#colocar o grafico aqui
], style={'width':'80%','margin':'0 auto'}
)
@app.callback(#uma função que vai ser chamada através de um evento
    Output('grafico_linguagem', 'figure'),
    [Input('dropdown_linguagens','value')]
    )
def scarter_linguagens(Linguagens_selecionadas):
    scarter_trace=[]
    for linguagem in Linguagens_selecionadas:
        dados_linguagens = dados_conceitos[linguagem]
        for conceito, conhecimento in dados_linguagens.items():
            scartter_trace.append(
                go.Scatter(
                x = [conceito],
                y = [conhecimento],
                mode = 'markers',
                name = linguagem.title(),
                marker = {'size':15, 'color':cores_map
                [linguagem]},
                showLegend = False
            )
        )
    scartter_layout = go.layout(
        title = "Meus conhecimentos em Linguagens",
        xaxis = dict(title = 'Conceitos', showgrid = False),
        yaxis = dict(title = 'Nivel de Conhecimento', showgrid = False)
    )
    
    return{'data':scartter_trace, 'layout':scartter_layout}

if __name__ == '__main__':
    app.run_server(debug=True)