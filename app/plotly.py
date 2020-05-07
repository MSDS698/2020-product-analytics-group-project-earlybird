import plotly
from plotly.graph_objs import Candlestick

def plotly_candle(df):

    data = [
        Candlestick(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])
    ]

    fig = dict(data=data)
    output = plotly.offline.plot(fig, include_plotlyjs=False,
                                 output_type='div')
    return output

if __name__=="__main__":
    plotly_candle()