from operator import itemgetter
import fitz
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextContainer, LTChar,LTLine,LAParams, LTTextLine, LTTextBox
from io import StringIO

keyword = 'Discussion'
Path = r"C:\Users\damojipurapuv.d\Downloads\Andrilli_AD_et_al_2009.pdf"
styles = {}
font_counts = {}
granularity=False
doc = fitz.open(Path)
for i in range(1,len(doc)+1):
    page = doc[i-1]
    blocks = page.get_text("dict")["blocks"]
    for b in blocks: # iterate through the text blocks
        if b['type'] == 0: # block contains text
            for l in b["lines"]: # iterate through the text lines
                for s in l["spans"]: # iterate through the text spans
                    if granularity:
                        identifier = "{0}_{1}_{2}_{3}".format(s['size'], s['flags'], s['font'], s['color'])
                        styles[identifier] = {'size': s['size'], 'flags': s['flags'], 'font': s['font'],
                        'color': s['color']}
                    else:
                        identifier = "{0}".format(s['size'])
                        styles[identifier] = {'size': s['size'], 'font': s['font']}

                    font_counts[identifier] = font_counts.get(identifier, 0) + 1 # count the fonts usage

font_counts = sorted(font_counts.items(), key=itemgetter(1), reverse=True)
#styles = sorted(styles.items(), key=itemgetter(1), reverse=True)
if len(font_counts) < 1:
    raise ValueError("Zero discriminating fonts found!")

#print(font_counts, styles)
p_style = styles[font_counts[0][0]] # get style for most used font by count (paragraph)
p_size = p_style['size']
print(p_size)


results = [] # list of tuples that store the information as (text, font size, font name)
total_data =[]
para_data =[]
search_data =[]
v={}
pdf = fitz.open(Path) # filePath is a string that contains the path to the pdf
for page in pdf:
    dict = page.get_text("dict")
    blocks = dict["blocks"]
    for block in blocks:
        if "lines" in block.keys():
            spans = block['lines']
            for span in spans:
                data = span['spans']
                for lines in data:
                    if lines['size']>=p_size:
                        total_data.append([[lines['text']], [lines['size'], lines['font']]])
                        search_data.append([[lines['text']], [str(int(lines['size']))]])
                        para_data.append([lines['text']])        #, [lines['size']]])
                    if keyword in lines['text']: # only store font information of a specific keyword
                        results.append([[lines['text']], [lines['size'], lines['font']]])
                        # lines['text'] -> string, lines['size'] -> font size, lines['font'] -> font name
pdf.close()
print(search_data)
print(results)
headers=['']
headers_info =[]
for line in total_data:
    if results[-1][1] == line[1]:
        headers_info.append(line)
        headers.extend(line[0])
print(headers)
header_size=(headers_info[0][1][0])

paragraph =[]
check =[]
str1 =''
for data in (para_data):
    paragraph.extend(data)
str2 = str1.join(paragraph)
for al in search_data:
    rec=(''.join(str(x) for x in al[1]))
    if float(rec) >=(p_size) or float(rec)>= header_size:
        check.extend(al[0])
str3 = str1.join(check)
#print(str3)

out = open("recent.txt", "wb")  # open text output
out.write(str2.encode("utf-8"))  # write text of page
out.write(bytes((12,)))
out.close()
for cols in range(2,len(headers)+1):
    start = headers[cols-2]    #.replace(' ','')  #'SUBJECTS AND METHODS'
    end = headers[cols-1]
    if start=='':  #.replace(' ','')
        res=(str2[str2.find(start)+len(start):str2.rfind(end)])
        print(start + ':'+ '    ' + res)
        print("\n\n")
    else:
        res=(str2[str2.rfind(start)+len(start):str2.rfind(end)])
        print(start + ':'+ '    ' + res)
        print("\n\n")



