import os, settings
import numpy as np
import pandas as pd

road_df = pd.read_csv(os.path.join(settings.BASE_DIR, 'output', "road_with_light.csv"), encoding='ms949')
print(road_df)