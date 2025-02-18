import plotly.graph_objs as graph_ob
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.dependencies import Input, Output
from dash import html, dcc, Input, Output

#configurando cores para os temas
dark_theme = 'darkly'
vapor_theme = 'vapor'
url_dark_theme = dbc.themes.DARKLY
url_vapor_theme = dbc.themes.VAPOR

#-------------------Dados----------------
#importando os dados da tabela csv
df = pd.read_csv('C:/Andre/Python_Dados/Aula 2/dataset_comp.csv')
df ['dt_Venda'] = pd.todatetime(df['dt_Venda'])
df['Mes'] = df['dt_Venda'].dt.strftime('%b').str.upper()

#-------------------Lista----------------
#criar lista de clientes 
lista_clientes = []
for cliente in df['Cliente'].unique():
    lista_clientes.append({
        'label': cliente,
        'value': cliente
    })
lista_clientes.append({
    'label':'Todos os clientes',
    'value':'todos_clientes'
})

#criando lista de meses 
meses_br = dict(
    JAN = 'JAN',
    FEV = 'FEV',
    MAR = 'MAR',
    APR = 'ABR',
    MAY = 'MAI',
    JUN = 'JUN',
    JUL = 'JUL',
    AUG = 'AGO',
    SEP = 'SET',
    OCT = 'OUT',
    NOV = 'NOV',
    DEC = 'DEZ'
)
lista_meses = [ ]
for mes in df['Mes'].unique( ):
    mes_pt = meses_br.get(mes, mes)
    
    lista_meses.append({
        'label': mes_pt,
        'value': mes    
    })

lista_meses.append({
    'label': 'Ano Completo',
        'value': 'ano_completo'
})

#Criando lista de categorias
lista_categorias = []
for categoria in df['Categoria'].unique():
    lista_categorias.append({
        'label': categoria,
        'value': categoria
    })
    
lista_categorias.append({
    'label':'Todas as Categotias',
    'value':'todas_categorias'
})
    
    
#Inicio do server
app = dash.Dash(__name__)
server = app.server

#---------------LAYOUT--------------- 
layout_titulo = html.Div([
    
    #elemento do select no superior esquerdo
    html.Div(
        dcc.Dropdown(
            id = 'dropdown_cliente',
            options = lista_clientes,
            placeholder = lista_clientes[-1]['label'],
            style = {
                'background-color' : 'transparent',
                'border': 'none',
                'color': 'black'
            }
        ), style = {'width': '25%'}
    ),
    html.Div(
        html.Legend(
            'Sebrae Maranhão',
            style = {
                'font-size':'150%',
                'text-align': 'center'
            }
        ), style = {'width': '50%'}
    ),
    html.Div(
        ThemeSwitchAIO(
            aio_id = 'theme',
            themes = [
                url_dark_theme,
                url_vapor_theme
            ]
        ), style = {'width': '25%'}
    )
], style = {
    'text-align': 'center',
    'display': 'flex',
    'justify-content':'space-around',
    'align-items': 'center',
    'font-family': 'Fira Code',
    'margin-top': '20px'
})

layout_linha01 = html.Div([
    html.Div([
        html.H4(id='output_cliente'),
        dcc.Graph(id = 'visual01')
], style = {
    'width':'¨65%',
    'text-align':'center'}
),

# primeira linha segunda coluna
html.Div([
    dbc.Cheklist(
        id = 'radio_mes',
        options = lista_meses,
        inline = True
    ),
    dbc.RadioItems(
        id = 'radio_categorias',
        options = lista_categorias,
        inline = True      
    )
],style = {
    'width': '30%',
    'display':'flex',
    'flex-direction': 'column',
    'justify-content': 'space-evenly'})
], style = {
    'display':'flex',
    'justify-content': 'space-around',
    'margin-top':'40px',
    'heigth': '300px'
})

layout_linha02 = html.Div([
    html.Div([
        html.H4('Vendas por mês e Loja/Cidade'),
        dcc.Graph(id = 'visual02')
    ],style={
        'width':'60%',
        'text-align':'center'
    }),
    html.Div(dcc.Graph(id='visual03'),stye={'width':'35%'})
],style ={
    'display':'flex',
    'justify-content':'space-around',
    'margim-top':'40px',
    'height':'150px'
})
#carregar o layout
app.layout = html.Div([
    layout_titulo,
    layout_linha01,
    layout_linha02
])


#---------------FUNÇÕES DE APOIO--------------- 
def filtro_cliente(cliente_selecionado):
    if cliente_selecionado is None:
        return pd.Series(True, index = df.index)
    return df['Cliente'] == cliente_selecionado

def filtro_categoria(categoria_selecionada):
    if categoria_selecionada is None:
        return pd.Series(True, index = df.index)
    elif categoria_selecionada == 'todas_categorias':
        return pd.Series(True, index = df.index)
    return df['Categorias'] == categoria_selecionada

def filtro_mes(meses_seleciondos):
    if not meses_seleciondos:
        return pd.Series(True, index = df.index)
    elif 'ano_completo' in meses_seleciondos:
        return pd.Series(True, index = df.index)
    else:
        return df['Mes'].isin(meses_seleciondos)


#---------------CALLBACKS--------------- 
@app.callback(
    Output('output_cliente','children'),
    [
        Input('dropdown_cliente','value')
        Input('radio_categorias','value')
    ]
)


#Subindo servidor 
if __name__ == 'main':
    app.run_server(debug = True)