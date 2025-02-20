import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import base64
import os

os.chdir(os.path.dirname(__file__))

#inicializando o app dash
app = dash.Dash(__name__)
#carrega para o dataset os dados de vendas
df = pd.read_csv('vendas.csv')
#cria a classe para a estrutura de analise de dados
class AnalisadorDeVendas:
    def __init__(self,dados):
        #inicializa a classe com o dataframe da tabela vendas
        self.dados = dados
        self.limpar_dados()

    def limpar_dados(self):
        #limpeza e preparação dos dados para analise com as demais funções
        self.dados['data'] = pd.to_datetime(self.dados['data'],errors='coerce')#converte as data em formato de texto para o formato datetime
        self.dados['valor'] = self.dados['valor'].replace({',','.'}, regex=True).astype(float)
        self.dados['mes'] = self.dados['data'].dt.month
        self.dados['ano'] = self.dados['data'].dt.year
        self.dados['dia'] = self.dados['data'].dt.day
        self.dados['dia_da_semana'] = self.dados['data'].dt.weekday
        #remove os dados ausentes em colunas
        self.dados.dropna(subset=['produto','valor'], inplace=True)
    
    def analise_vendas_por_Produto(self, produtosFiltrados):
        df_produto = self.dados[self.dados['produto'].isin(produtosFiltrados)]
        df_produto = df_produto.groupby(['produto'])['valor'].sum().reset_index().sort_values(by='valor', ascending=True)
        fig = px.bar(
            df_produto,
            x= 'produto',
            y= 'valor',
            title= "Vendas por Produto",
            calor= "valor"
        )
        return fig

#------------------- Instanciar o objeto de analise de vendas-------------------#
analise = AnalisadorDeVendas(df)
#------------------- layout do app dash -------------------#
app.layout = html.Div([
    html.H1('Análise de Vendas', style={'text-align': 'center'}),
    #cria os filtros de seleção para o painel
    html.Div([
        html.Label('Selecione os produtos'),
        dcc.Dropdown(
            id='produto-dropdwon',
            options = [Output{'label':produto,'value':produto} for produto in df['produto'].unique],
            multi = True,
            value = df['produto'].unique().tolist(),
            style={'width':'48%'}            
        ),
        
        html.Label('Selecione as Regiões:'),
        dcc.Dropdown(
            id='regiao-dropdwon',
            options = [Output{'label':regiao,'valor':regiao} for regiao 
            in df['regiao'].unique],
            multi = True,
            value = df['regiao'].unique().tolist(),
            style={'width':'48%'}            
        ),
    
        html.label('Selecione o Ano:'),
            dcc.Dropdown(
                id='ano-dropdwon',
                options = [{'label':str(ano),'value':ano} for ano in df['ano'].unique],
                value = df['ano'].min(),
                style={'width':'48%'}            
            ),

        html.label('Selecione um periodo:'),
            dcc.DatePickerRange(
                id='data-picker-range',
                start_date=df['data'].min().date(),
                end_date=df['data'].max().date(),
                dispay_format='DD/MM/YY'
                style={'width':'48%'}            
            ),
    ],style={'padding':'20px'}),
    #graficos
    html.Div([
        dcc.Graph(id='grafico-produto')
    ])
])
#------------------- Callbacks -------------------#
@app.callback(
    Output('grafico-produto','figure'),
    Input('produto-dropdown','value'),
    Input('regiao-dropdown','value'),
    Input('ano-dropdown','value'),
    Input('date-picker-range','start-date'),
    Input('date-picker-range','end-date')
)
def upgrade_graphs(produtos,regioes,ano,star_date,end_date):
    try:
        #converte a data para o fomato correto
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        #atualizar os graficos de acordo com
        fig_produto = analise.analise_vendas_por_produto(produtos)
    except Exception as e:
        #sempre que ocorrer algum erro, mostrar a mensagem de erro e retorna
        print(f'Erro ao atualizar os graficos: {str(e)}')
        return go.Figure()

#roda o app
if __name__ == '__main__':
    app.run_server(debug=True)