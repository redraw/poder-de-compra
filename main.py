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

# ----- Poder de Compra -----
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

pdc.to_json("index.json")
pdc.plot(log_y=True).write_html("index.html")

# ----- Dolar -----
dolar = pd.read_json("https://api.argentinadatos.com/v1/cotizaciones/dolares", convert_dates=["fecha"])
dolar = dolar.set_index("fecha")
dolar_blue = dolar[dolar.casa == "blue"]

# tipo de cambio BLUE venta promedio mensual
tc = dolar_blue["venta"].resample("MS").mean()

# series dolarizadas mínimas
ripte_usd = (ripte["ripte"] / tc).dropna()
smvm_usd = (smvm["salario_minimo_vital_movil_mensual"] / tc).dropna()

# ----- Salarios -----
salarios_usd = pd.concat({"RIPTE": ripte_usd, "SMVM": smvm_usd}, axis=1)

salarios_usd.to_json("salarios.json")
salarios_usd.plot(title="Salarios (USD blue)", log_y=True).write_html("salarios.html")

# ----- Canastas -----
can_nac_usd = canasta[["canasta_basica_alimentaria","canasta_basica_total"]].div(tc, axis=0).dropna(how="all")
can_caba_usd = canasta_caba[["canasta_basica_alimentaria","canasta_basica_total"]].div(tc, axis=0).dropna(how="all")

canastas_usd = (can_nac_usd.add_suffix("_nacional")
                .join(can_caba_usd.add_suffix("_CABA")))

canastas_usd.to_json("canastas.json")
canastas_usd.plot(title="Canastas (USD blue)", log_y=True).write_html("canastas.html")
