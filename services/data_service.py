import pandas as pd

def read(fname):
    columns = {
           "potential_flux": 2,
           "absorbed_flux": 3,
           "cos_factor": 4,
           "shadow_losses": 5,
           "missing_losses": 6,
           # "reflectivity_losses": 7,
           # "absorptivity_losses": 8
           }
    df = pd.read_csv(fname, sep='\s+', names=range(47))
    df_out = df.loc[df[1] == 'Sun', [3]]  # azimuth (transversal plane)
    df_out.columns = ["azimuth"]
    df_out["zenith"] = df.loc[df[1] == 'Sun', [4]]
    df_out["efficiency"] = df.loc[df[0] == 'absorber', [23]].values
    for key in columns.keys():
        df_out[key] = df[0].iloc[df_out.index + \
                                 columns.get(key)].astype('float').values
    return df_out