import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.io as pio

pio.templates.default = "simple_white"

def make_bar_chart(dataset, categrical_col, start_year, end_year, title, frame_rate=3):
    names = dataset[categrical_col]
    yvals = dataset.loc[:, start_year]

    def get_rgb_vals():
        r = np.random.randint(1, 255)
        g = np.random.randint(1, 255)
        b = np.random.randint(1, 255)
        return [r, g, b]

    colors = []
    for i in range(len(names)):
        c = get_rgb_vals()
        colors.append("rgb(" + str(c[0]) + "," + str(c[1]) + "," + str(c[2]) + ")")

    def get_top_10(d):
        df = pd.DataFrame({"names": names, "pop": d, "color": colors})
        # features = df.sort_values(by = "pop").iloc[-15:,]
        return df

    listOfFrames = []
    for i in range(int(start_year), int(end_year) + 1, frame_rate):
        d = dataset.loc[:, str(i)]
        pdata = get_top_10(d)
        listOfFrames.append(go.Frame(data=[go.Bar(x=pdata["names"], y=pdata["pop"],
                                                  marker_color=pdata["color"], text=pdata["names"],
                                                  hoverinfo="none", textposition="outside",
                                                  texttemplate="%{x}<br>%{y:s}", cliponaxis=False)],
                                     layout=go.Layout(
                                         font={"size": 20},
                                         height=700,
                                         xaxis={"showline": False, "tickangle": -90, "visible": False},
                                         yaxis={"showline": False, "visible": False},
                                         title=title + " For: " + str(i))))

    fData = get_top_10(yvals)

    fig = go.Figure(
        data=[go.Bar(x=fData["names"], y=fData["pop"],
                     marker_color=fData["color"], text=fData["names"],
                     hoverinfo="none", textposition="outside",
                     texttemplate="%{x}<br>%{y:s}", cliponaxis=False)],
        layout=go.Layout(
            title=title + " For: " + str(start_year),
            font={"size": 20},
            height=700,
            xaxis={"showline": False, "tickangle": -90, "visible": False},
            yaxis={"showline": False, "visible": False},
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])]
        ),
        frames=list(listOfFrames)
    )
    fig.show()
