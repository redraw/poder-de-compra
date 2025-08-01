import pandas as pd

pd.options.plotting.backend = "plotly"

ripte = pd.read_csv(
    "https://infra.datos.gob.ar/catalog/sspm/dataset/158/distribution/158.1/download/remuneracion-imponible-promedio-trabajadores-estables-ripte-total-pais-pesos-serie-mensual.csv",
    parse_dates=["indice_tiempo"],
    index_col="indice_tiempo",
)
canasta = pd.read_csv(
    "https://infra.datos.gob.ar/catalog/sspm/dataset/150/distribution/150.1/download/valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv",
    parse_dates=["indice_tiempo"],
    index_col="indice_tiempo",
)

canasta_caba = pd.read_csv(
    "https://infra.datos.gob.ar/catalog/sspm/dataset/444/distribution/444.1/download/canastas-basicas-ciudad-de-buenos-aires.csv",
    parse_dates=["indice_tiempo"],
    index_col="indice_tiempo",
)

pdc = pd.DataFrame()
pdc["CBA"] = ripte.ripte / canasta.canasta_basica_alimentaria
pdc["CBT"] = ripte.ripte / canasta.canasta_basica_total
pdc["CBA_CABA"] = ripte.ripte / canasta_caba.canasta_basica_alimentaria
pdc["CBT_CABA"] = ripte.ripte / canasta_caba.canasta_basica_total
pdc.to_json("data.json")

fig = pdc.loc["2013":].plot(log_y=True)
fig.write_html("index.html")
