import pypsa
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.width', 1000000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', '{:.5f}'.format)

def getIndexDe (df):
  return df.index.str.startswith('DE0')

def getBus0De (df):
  return df['bus0'].str.startswith('DE0')

def getBus1De (df):
  return df['bus1'].str.startswith('DE0')

def getDeExport (df):
  return (df['bus1'].str.startswith('DE0')) & (~(df['bus0'].str.startswith('DE0')))

def getDeImport (df):
  return (~(df['bus1'].str.startswith('DE0'))) & (df['bus0'].str.startswith('DE0'))

def getTheCarrier (df , carrier):
  return (df['carrier'] == carrier)

def getIndexDeCarrier (df , carrier):
  return getIndexDe(df) & getTheCarrier(df, carrier)

def getIndexSeries(df, condition):
  return df[condition].index.to_series()

def getEmptyIndex ():
  return pd.Index([]).to_series()

def replaceCarrier (df, old, new): 
  df['carrier'] = df['carrier'].replace(old, new)
  return df

def de_grouper(n, c):
  if (c == 'Line'):
    dfLine = n.df(c)
    indexsLine = dfLine[dfLine['bus1'].str.startswith('DE0')].index.to_series()
    return indexsLine

  if (c == 'Link'):
    dfLink = n.df(c)
    indexsLink = dfLink[(dfLink['bus1'].str.startswith('DE0')) 
                        | ((dfLink['bus0'].str.startswith('DE0') & dfLink['bus1'].str.startswith('EU')))
                      ].index.to_series()
    return indexsLink

  df = n.df(c)
  return df[df.index.str.startswith('DE0')].index.to_series()
pypsa.statistics.groupers.add_grouper("de_grouper", de_grouper)

def de_import_elec_grouper(n, c):
  if (c == 'Line'):
    dfLine = n.df(c)
    return dfLine[dfLine['bus1'].str.startswith('DE0') 
                  & (~(dfLine['bus0'].str.startswith('DE0')))].index.to_series()
  
  if (c == 'Link'):
    dfLink = n.df(c)
    return dfLink[(dfLink['bus1'].str.startswith('DE0')) 
                  & (dfLink['carrier'] == 'DC') 
                  & (~(dfLink['bus0'].str.startswith('DE0')))].index.to_series()

  return pd.Index([]).to_series()
pypsa.statistics.groupers.add_grouper("de_import_elec_grouper", de_import_elec_grouper)

def de_export_elec_grouper(n,c):
  if (c == 'Line'):
    dfLine = n.df(c)
    return dfLine[(dfLine['bus0'].str.startswith('DE0')) 
                  & (~(dfLine['bus1'].str.startswith('DE0')))].index.to_series()
  
  if (c == 'Link'):
    dfLink = n.df(c)
    return dfLink[(dfLink['bus0'].str.startswith('DE0')) 
                  & (dfLink['carrier'] == 'DC')  
                  & (~(dfLink['bus1'].str.startswith('DE0')))].index.to_series()

  return pd.Index([]).to_series()
pypsa.statistics.groupers.add_grouper("de_export_elec_grouper", de_export_elec_grouper)

def de_import_h2_grouper(n,c):
  if (c == 'Link'):
    dfLink = n.df(c)
    return dfLink[(dfLink['bus1'].str.startswith('DE0')) 
                  & (dfLink['carrier'] == 'H2 pipeline') 
                  & (~(dfLink['bus0'].str.startswith('DE0')))].index.to_series()
  
  return pd.Index([]).to_series()
pypsa.statistics.groupers.add_grouper("de_import_h2_grouper", de_import_h2_grouper)

def de_export_h2_grouper(n,c):
  if (c == 'Link'):
    dfLink = n.df(c)
    return dfLink[(dfLink['bus0'].str.startswith('DE0')) 
                  & (dfLink['carrier'] == 'H2 pipeline')  
                  & (~(dfLink['bus1'].str.startswith('DE0')))].index.to_series()
  
  return pd.Index([]).to_series()
pypsa.statistics.groupers.add_grouper("de_export_h2_grouper", de_export_h2_grouper)

def de_generator_grouper(n,c):
  if ( c == 'Generator'):
    df = n.df(c)
    index =  df[((df.index.str.startswith('DE0')) & (df['carrier'] == 'nuclear')) |
              # ((df.index.str.startswith('DE0')) & (df['carrier'] == 'gas')) |
              # ((df.index.str.startswith('DE0')) & (df['carrier'] == 'biogas')) |
              ((df.index.str.startswith('DE0')) & (df['carrier'] == 'urban central solid biomass CHP')) |
              ((df.index.str.startswith('DE0')) & (df['carrier'] == 'offwind-ac')) |
              ((df.index.str.startswith('DE0')) & (df['carrier'] == 'offwind-dc')) |
              ((df.index.str.startswith('DE0')) & (df['carrier'] == 'offwind-float')) |
              ((df.index.str.startswith('DE0')) & (df['carrier'] == 'onwind')) |
              ((df.index.str.startswith('DE0')) & (df['carrier'] == 'ror')) |
              ((df.index.str.startswith('DE0')) & (df['carrier'] == 'solar')) |
              ((df.index.str.startswith('DE0')) & (df['carrier'] == 'solar rooftop')) |
              ((df.index.str.startswith('DE0')) & (df['carrier'] == 'solar-hsat'))
            ].index.to_series()
    return index
  
  if ( c == 'Link'):
    df = n.df(c)
    index =  df[((df['bus0'].str.startswith('DE0')) & (df['carrier'] == 'OCGT')) |
              ((df['bus0'].str.startswith('DE0')) & (df['carrier'] == 'H2 Fuel Cell')) |
              ((df['bus0'].str.startswith('DE0')) & (df['carrier'] == 'urban central solid biomass CHP')) |
              ((df['bus0'].str.startswith('DE0')) & (df['carrier'] == 'urban central CHP')) |
              ((df['bus0'].str.startswith('DE0')) & (df['carrier'] == 'geothermal organic rankine cycle')) 
              ].index.to_series()
    return index
  return getEmptyIndex()
pypsa.statistics.groupers.add_grouper("de_generator_grouper", de_generator_grouper)


def de_heat_generator_grouper(n,c):
  if (c =='Generator'):
    df = n.df(c)
    return getIndexSeries(df, getIndexDeCarrier(df, 'rural solar thermal') |
             getIndexDeCarrier(df, 'urban central solar thermal') |
             getIndexDeCarrier(df, 'urban decentral solar thermal') 
            )

  if (c == 'Link'):
    df = n.df(c)
    return getIndexSeries(df, 
                      getIndexDeCarrier(df, 'urban decentral gas boiler') |
                        getIndexDeCarrier(df, 'urban decentral biomass boiler') |
                        getIndexDeCarrier(df, 'urban decentral air heat pump') |
                        getIndexDeCarrier(df, 'urban decentral resistive heater') |
                        getIndexDeCarrier(df, 'urban central solid biomass CHP') |
                        getIndexDeCarrier(df, 'urban central resistive heater') |
                        getIndexDeCarrier(df, 'urban central gas boiler') |
                        getIndexDeCarrier(df, 'urban central air heat pump') |
                        getIndexDeCarrier(df, 'urban central CHP') |
                        getIndexDeCarrier(df, 'rural resistive heater') |
                        getIndexDeCarrier(df, 'rural ground heat pump') |
                        getIndexDeCarrier(df, 'rural gas boiler') |
                        getIndexDeCarrier(df, 'rural biomass boiler') |
                        getIndexDeCarrier(df, 'rural air heat pump') |
                        getIndexDeCarrier(df, 'geothermal heat') |
                        getIndexDeCarrier(df, 'geothermal district heat') 
                      )
  return getEmptyIndex()
pypsa.statistics.groupers.add_grouper("de_heat_generator_grouper", de_heat_generator_grouper)

def de_biogas_generator_grouper(n, c):
  if (c =='Generator'):
    df = n.df(c)
    return getIndexSeries(df, getIndexDeCarrier(df, 'biogas'))
  return getEmptyIndex()
pypsa.statistics.groupers.add_grouper("de_biogas_generator_grouper", de_biogas_generator_grouper)

def de_gas_generator_grouper(n,c):
  if (c =='Generator'):
    df = n.df(c)
    return getIndexSeries(df, getIndexDeCarrier(df, 'gas'))
  
  if (c == 'Link'):
    df = n.df(c)
    return getIndexSeries(df, 
                      getIndexDeCarrier(df, 'Sabatier') |
                      getIndexDeCarrier(df, 'biogas to gas')
                      )
  return getEmptyIndex()
pypsa.statistics.groupers.add_grouper("de_gas_generator_grouper", de_gas_generator_grouper)

def de_phs_grouper(n, c):
  if (c == "StorageUnit"):
    df = n.df(c)
    return getIndexSeries(df, 
                      getIndexDeCarrier(df, 'PHS')
                      )
  return getEmptyIndex()
pypsa.statistics.groupers.add_grouper("de_phs_grouper", de_phs_grouper)

def de_elec_store_grouper(n, c):
  if (c == "StorageUnit"):
    df = n.df(c)
    return getIndexSeries(df, 
                      getIndexDeCarrier(df, 'PHS') | 
                      getIndexDeCarrier(df, 'hydro')
                      )
  if (c == 'Store'):
    df = n.df(c)
    return getIndexSeries(df,
                         getIndexDeCarrier(df, 'EV battery') | 
                         getIndexDeCarrier(df, 'battery') | 
                         getIndexDeCarrier(df, 'home battery')
                        )
  return getEmptyIndex()
pypsa.statistics.groupers.add_grouper("de_elec_store_grouper", de_elec_store_grouper)

def de_h2_to_elc_gropuer(n,c):
  if ( c == 'Link'):
    df = n.df(c)
    return getIndexSeries(df,
                         getIndexDeCarrier(df, 'H2 Fuel Cell') 
                        )
  return getEmptyIndex()
pypsa.statistics.groupers.add_grouper("de_h2_to_elc_gropuer", de_h2_to_elc_gropuer)

def de_elc_to_h2_grouper(n,c):
  if ( c == 'Link'):
    df = n.df(c)
    return getIndexSeries(df,
                         getIndexDeCarrier(df, 'H2 Electrolysis') 
                        )
  return getEmptyIndex()
pypsa.statistics.groupers.add_grouper("de_elc_to_h2_grouper", de_elc_to_h2_grouper)


def de_elec_use_grouper(n,c):
  if (c == 'Load'):
    df = n.df(c)
    return getIndexSeries(df,
                          getIndexDeCarrier(df, 'agriculture electricity') |
                          getIndexDeCarrier(df, 'electricity') |
                          getIndexDeCarrier(df, 'industry electricity')  
                          )
  if (c == 'Link'):
    df = n.df(c)
    return getIndexSeries(df,
                          getIndexDeCarrier(df, 'urban central air heat pump') |
                          getIndexDeCarrier(df, 'urban central resistive heater') |
                          getIndexDeCarrier(df, 'rural air heat pump') |
                          getIndexDeCarrier(df, 'rural ground heat pump') |
                          getIndexDeCarrier(df, 'rural resistive heater') |
                          getIndexDeCarrier(df, 'urban decentral air heat pump') |
                          getIndexDeCarrier(df, 'urban decentral resistive heater') |
                          getIndexDeCarrier(df, 'urban decentral resistive heater') |
                          getIndexDeCarrier(df, 'DAC') 
                          )
  return getEmptyIndex()
pypsa.statistics.groupers.add_grouper("de_elec_use_grouper", de_elec_use_grouper)


def de_elec_charge_grouper(n, c):
  if (c == 'Link'):
    df = n.df(c)
    return getIndexSeries(df,
                          getIndexDeCarrier(df, 'BEV charger') |
                          getIndexDeCarrier(df, 'urban central air heat pump') |
                          getIndexDeCarrier(df, 'urban central resistive heater') |
                          getIndexDeCarrier(df, 'urban central resistive heater')    
                          )

def eu_grouper(n, c):
  df = n.df(c)
  print('----------------',c)
  print(df.groupby('carrier').size())
  indexs = df[df.index.astype(str).str.contains('EU')].index.to_series()
  return indexs
pypsa.statistics.groupers.add_grouper("eu_grouper", eu_grouper)

def dataframe_to_table(df):
    df = df.fillna('/')
    result_list = []
    for index, row in df.iterrows():
        formatted_elements = []
        formatted_elements.append(f'[{index}]')
        for item in row:
            if isinstance(item, float):
                formatted_elements.append(f'[{item:.3f}]')  
            else:
                formatted_elements.append(f'[{item}]')
        formatted_row = ', '.join(formatted_elements)
        result_list.append(f'  {formatted_row},') 
    return '\n'.join(result_list)

def renameHeatCarrier (df):
  df.rename(index={'geothermal district heat': 'Geothermie'}, inplace=True)
  df.rename(index={'geothermal heat': 'Geothermie'}, inplace=True)
  df.rename(index={'rural air heat pump': 'Strom zu Wärme'}, inplace=True)
  df.rename(index={'rural biomass boiler': 'Biomassekessel'}, inplace=True)
  df.rename(index={'rural gas boiler': 'Gaskessel'}, inplace=True)
  df.rename(index={'rural ground heat pump': 'Strom zu Wärme'}, inplace=True)
  df.rename(index={'rural resistive heater': 'Strom zu Wärme'}, inplace=True)
  df.rename(index={'rural resistive heater': 'Solarthermie'}, inplace=True)
  df.rename(index={'rural solar thermal': 'Solarthermie'}, inplace=True)
  df.rename(index={'urban central CHP': 'Gas CHP'}, inplace=True)
  df.rename(index={'urban central air heat pump': 'Strom zu Wärme'}, inplace=True)
  df.rename(index={'urban central gas boiler': 'Gaskessel'}, inplace=True)
  df.rename(index={'urban central resistive heater': 'Strom zu Wärme'}, inplace=True)
  df.rename(index={'urban central solar thermal': 'Solarthermie'}, inplace=True)
  df.rename(index={'urban central solid biomass CHP': 'Biomasse CHP'}, inplace=True)
  df.rename(index={'urban decentral air heat pump': 'Strom zu Wärme'}, inplace=True)
  df.rename(index={'urban decentral biomass boiler': 'Biomassekessel'}, inplace=True)
  df.rename(index={'urban decentral gas boiler': 'Gaskessel'}, inplace=True)
  df.rename(index={'urban decentral resistive heater': 'Strom zu Wärme'}, inplace=True)
  df.rename(index={'urban decentral solar thermal': 'Solarthermie'}, inplace=True)

  return df.groupby('carrier').sum()

def getDiffTableColum (cb, scenarios):
  result = {}
  for scenario in scenarios:
    result[scenario.name] = cb(scenario.n)
  
  return result