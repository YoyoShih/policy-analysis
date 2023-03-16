import xlwings as xw

''' Input '''
# df: the dataframe that would be output to excel
def opExcel(df):
    with xw.APP(visible=True, add_book=False) as app:
        app.display_alerts = False
        app.screen_updating = False
        