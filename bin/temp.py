import pdfplumber
import pandas as pd

with pdfplumber.open('C:\\Users\\shih\\ActuaViz\\docs\\excel\\69359449877827.pdf') as pdf:
    table_settings = {
        "vertical_strategy": "text",
        "horizontal_strategy": "text",
        "snap_y_tolerance": 5,
        "intersection_x_tolerance": 15,
    }
    a = 1
    for page in pdf.pages:
        table = page.extract_table(table_settings)
        table_df = pd.DataFrame(table,columns=['x', 'l', 'd', 'q', 'e', 'L', 'T'])
        table_df.to_csv(f'{a}.csv')
        a += 1