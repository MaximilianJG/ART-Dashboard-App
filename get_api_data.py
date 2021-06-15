import pandas as pd
import numpy as np
import requests

def get_overlayed_zscore_data(participant_id):
    url = "https://art-api-n3bfhtw63q-ew.a.run.app/overlayed_zscores"
    params = {
        "participant_id": participant_id,
    }
    
    response = requests.get(url, params=params)
    json_df = pd.read_json(response.json())
    
    return json_df
