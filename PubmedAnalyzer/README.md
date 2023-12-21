# Pubmed Search Analyzer
 
This program can populate a sorted table with relevant information from Pubmed search files.

Here are instructions how to use it.
1. Search the author on Pubmed. Add "[Author]" after the search term to search only authors
2. Click on the save button under the search bar.
	Select "All results" for selection (not "All results on this page")
	Select "Pubmed" for format and create the file.
3. Rename the downloaded text file to a required part of the author's name, such as their last name
	Place extra parts or different representations of their name in parenthesis, separated by commas
	If two authors both contain the required part, the enclosed terms will be used to differentiate them
	For example, you can use "Smith (John C, John, Jack).txt" for either John C Smith or Jack C Smith

4. Move the file into the "Export Files" folder. The program will extract info from this folder.
	Only proceed once all of the text files are in this folder

6. Run the "PubmedAnalyzer.py" script
	In windows, you can run it through double-clicking the Run Me.bat file
	In both windows and Mac/Linux, you can directly run the .py file with command prompt/terminal
7. The "compiled.csv" file will be rewritten with the result. Check for any irregularities.
	This file will be overwritten each time the script is run.

Notes: Special characters will interfere with the analysis. Please replace all special characters
with a text-editing program. For example, "Peña" can be replaced with "Pena"