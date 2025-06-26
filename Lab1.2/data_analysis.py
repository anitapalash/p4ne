import openpyxl as xl
from matplotlib import pyplot

TEMP_STR = 'Температура\Активность Солнца'
YEAR_STR = 'Год'

def get_value(cell):
    return cell.value

wb = xl.load_workbook('../materials/data_analysis_lab.xlsx')
sheet = wb['Data']
colA = sheet['A'][1:]
colC = sheet['C'][1:]
colD = sheet['D'][1:]
listA = list(map(get_value, colA))
listC = list(map(get_value, colC))
listD = list(map(get_value, colD))

pyplot.plot(listA, listC, color='blue', label=YEAR_STR)
pyplot.plot(listA, listD, color='orange', label=TEMP_STR)
pyplot.legend()
pyplot.xlabel(YEAR_STR)
pyplot.ylabel(TEMP_STR)

pyplot.show()

