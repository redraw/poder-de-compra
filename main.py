import pandas as pd

pd.options.plotting.backend = "plotly"

ripte = pd.read_csv(
    "https://infra.datos.gob.ar/catalog/sspm/dataset/158/distribution/158.1/download/remuneracion-imponible-promedio-trabajadores-estables-ripte-total-pais-pesos-serie-mensual.csv",
    parse_dates=["indice_tiempo"],
    index_col="indice_tiempo",
)

smvm = pd.read_csv(
    "https://infra.datos.gob.ar/catalog/sspm/dataset/57/distribution/57.1/download/indice-salario-minimo-vital-movil-valores-mensuales-pesos-corrientes-desde-1988.csv",
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
pdc["RIPTE_CBA"] = ripte.ripte / canasta.canasta_basica_alimentaria
pdc["RIPTE_CBT"] = ripte.ripte / canasta.canasta_basica_total
pdc["RIPTE_CBA_CABA"] = ripte.ripte / canasta_caba.canasta_basica_alimentaria
pdc["RIPTE_CBT_CABA"] = ripte.ripte / canasta_caba.canasta_basica_total
pdc["SMVM_CBA"] = smvm.salario_minimo_vital_movil_mensual / canasta.canasta_basica_alimentaria
pdc["SMVM_CBT"] = smvm.salario_minimo_vital_movil_mensual / canasta.canasta_basica_total
pdc["SMVM_CBA_CABA"] = smvm.salario_minimo_vital_movil_mensual / canasta_caba.canasta_basica_alimentaria
pdc["SMVM_CBT_CABA"] = smvm.salario_minimo_vital_movil_mensual / canasta_caba.canasta_basica_total
pdc = pdc.dropna(how="all")

# export JSON
pdc.to_json("data.json")

# export plot
fig = pdc.plot(log_y=True)
fig.write_html("index.html")
