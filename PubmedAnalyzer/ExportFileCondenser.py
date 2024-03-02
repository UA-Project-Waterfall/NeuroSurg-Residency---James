from pathlib import Path
from PubmedAnalyzer import PubmedReader

fileDir = Path.joinpath(Path(__file__).parent.resolve(), "Export Files")
fileList = list(fileDir.glob('*.txt'))
include = ["pmid", "ti", "fau", "au", "ad", "jt", "ta", ""]
resultDir = Path.joinpath(Path(__file__).parent.resolve(), "Condensed Exports")
resultDir.mkdir(exist_ok = True, parents = True)

for filePath in fileList:
    lines = [line[0] + line[1] + "\n" for line in PubmedReader(filePath).lines if line[0][:4].strip().lower() in include]
    with open(Path.joinpath(resultDir, filePath.stem + " - Condensed.txt"), "w", newline = "", encoding = 'utf-8') as file:
        file.writelines(lines)