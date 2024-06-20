from pandas import read_excel
from pathlib import Path
import plotly.express as px

affMapFile = "AffiliationInfo.xlsx"
resMapFile = "ResidencyInfo.xlsx"

inputs = {
    "file": resMapFile,
    "startAt": 7
    }

filePath = Path.joinpath(Path(__file__).parent.resolve(), inputs["file"])
dataframe = read_excel(filePath)
for header in list(dataframe)[inputs["startAt"]:]:
    #dataframe["Count"] **= 2

    fig = px.density_mapbox(dataframe, lat = 'Latitude', lon = 'Longitude', z = header, title=header, labels={header:""},
                            radius = 30, zoom = 3.5, center = {"lat": 38, "lon": -105},
                            mapbox_style = 'open-street-map', color_continuous_scale=px.colors.sequential.Turbo)
    fig.show()