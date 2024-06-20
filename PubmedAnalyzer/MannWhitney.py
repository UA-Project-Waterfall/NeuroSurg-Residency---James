from pandas import read_excel
import openpyxl
from scipy.stats import mannwhitneyu
import tkinter as tk

filePath = ""
colNames = []

if filePath == ""
    tk.Tk().withdraw()
    filePath = tk.filedialog.askopenfilename()

data = pd.read_excel(filePath)
print(list(data.columns))


# Perform Mann-Whitney U test
statistic, p_value = mannwhitneyu(list(data[colNames[0]]), list(data[colNames[1]]))

# Output the results
print("Mann-Whitney U statistic:", statistic)
print("p-value:", p_value)

if p_value < 0.05:
    print("The difference between the groups is statistically significant.")
else:
    print("There is no statistically significant difference between the groups.")