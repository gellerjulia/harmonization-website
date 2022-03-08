import pandas as pd
import numpy as np
from datasets.models import RawNHANES_BIO, RawNHANES_LLOD
from api.dilutionproc import predict_dilution
from api.analysis import add_confound
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels


def get_dataframe_orig():
    """Returns a pandas DataFrame"""

    # First is necessary to pivot the raw NEU dataset so it matches
    # the requested features.

    # This queries the RawNEU dataset and excludes some of the values
    df = pd.DataFrame.from_records(
        RawNHANES_BIO.objects.
        # exclude(Creat_Corr_Result__lt=-1000).
        # exclude(Creat_Corr_Result__isnull=True).
        values()
    )
    
    ##only including pregnant participants
    df_preg=df[df['Pregnant']==1.0]

    ##Only including participants ages 18-40
    #df_preg=df_preg[df_preg['Age'] >=18]
    #df_preg=df_preg[df_preg['Age'] <=40]

    ## new covariates
    df_preg['Member_c'] = 1
    df_preg.columns = ['PIN_Patient', 'BLOD','Result', 'Analyte', 'Pregnant' , 'Age', 'Marital',
                  'Child_A', 'Child_B','H_Inc', 'F_Inc', 'Edu', 'Rac', 'TimePeriod', 'Member_c']
    numerical_values = 'Result'

    columns_to_indexes = ['PIN_Patient', 'TimePeriod', 'Member_c' ]
    categorical_to_columns = ['Analyte']

    df_preg = pd.pivot_table(df_preg, values=numerical_values,
                        index=columns_to_indexes,
                        columns=categorical_to_columns)

    df_preg = df_preg.reset_index()
   
    

    # After pivot
    # Analyte     TimePeriod Member_c       BCD  ...      UTMO       UTU       UUR
    # PIN_Patient                                ...
    # A0000M               1        1  1.877245  ...  0.315638  1.095520  0.424221
    # A0000M               3        1  1.917757  ...  0.837639  4.549155  0.067877
    # A0001M               1        1  1.458583  ...  0.514317  1.262910  1.554346
    # A0001M               3        1  1.365789  ...  0.143302  1.692582  0.020716
    # A0002M               1        1  1.547669  ...  0.387643  0.988567  1.081877

    df_preg['CohortType'] = 'NHANES'
    
    return df_preg


def get_dataframe_orig_blod():
    """Returns a pandas DataFrame"""

    # First is necessary to pivot the raw NEU dataset so it matches
    # the requested features.

    # This queries the RawNEU dataset and excludes some of the values
    df = pd.DataFrame.from_records(
        RawNHANES_BIO.objects.
        # exclude(Creat_Corr_Result__lt=-1000).
        # exclude(Creat_Corr_Result__isnull=True).
        values()
    )
    
    
    
    
    ##only including pregnant participants
    df_preg=df[df['Pregnant']==1.0]

    ##Only including participants ages 18-40
    ##df_preg=df_preg[df_preg['Age'] >=18]
    ##df_preg=df_preg[df_preg['Age'] <=40]

    ## new covariates
    df_preg['Member_c'] = 1
    df_preg.columns = ['PIN_Patient', 'BLOD','Result', 'Analyte', 'Pregnant' , 'Age', 'Marital',
                  'Child_A', 'Child_B','H_Inc', 'F_Inc', 'Edu', 'Rac', 'TimePeriod', 'Member_c']

    #ga at collection

    # Pivoting the table and reseting index
    numerical_values = 'BLOD'

    columns_to_indexes = ['PIN_Patient', 'TimePeriod', 'Member_c' ]
    categorical_to_columns = ['Analyte']

    df_preg = pd.pivot_table(df_preg, values=numerical_values,
                        index=columns_to_indexes,
                        columns=categorical_to_columns)
                        
    df_preg = df_preg.reset_index()
    
    ##turning 9999.0 values into NaN
    for col in df_preg: 
        if col not in ['PIN_Patient', 'TimePeriod', 'Member_c', 'CohortType', 'Analyte']:
            df_preg[col]= df_preg[col].replace(9999.0, np.NaN)
   

    # After pivot
    # Analyte     PIN_Patient      Member_c     TimePeriod       UCO     UNI     .....                                ...
    #             A0000M           1             2017-18          1      0       ... 
    #             A0000M           1             2017-18          0      0       ... 
    #             A0000M           1             2017-18          0      NaN       ... 

    df_preg['CohortType'] = 'NHANES'
    #df['TimePeriod'] = pd.to_numeric(df['TimePeriod'], errors='coerce')
    
    return df_preg
