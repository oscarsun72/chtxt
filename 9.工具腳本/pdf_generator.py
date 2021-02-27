#!/usr/bin/env python3
# PDF generator for https://github.com/bgc2017/chtxt 

import re
import sys
from os.path import basename
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from  reportlab.platypus.tableofcontents import TableOfContents
from  reportlab.platypus import PageBreak,Spacer
from reportlab.lib.pagesizes import A4

bridge=False

pdfmetrics.registerFont(TTFont('Kaiti', 'Kaiti.ttf'))

styles = getSampleStyleSheet()
# styles for book / author / chapter / subsection / content /footer | up/right/down/left 
styles.add(ParagraphStyle(fontName='Kaiti', name='book', textColor="#FF0000",borderPadding=(100, 100, 100,20), leading=25, fontSize=36, wordWrap='CJK',alignment=1 ))
styles.add(ParagraphStyle(fontName='Kaiti', name='author', textColor="#9966FF",borderPadding=(110, 0, 20,120), leading=25, fontSize=12, wordWrap='CJK',alignment=2))
styles.add(ParagraphStyle(fontName='Kaiti', name='chapter', textColor="red",borderPadding=24, leading=25, fontSize=20, wordWrap='CJK',alignment=1))
styles.add(ParagraphStyle(fontName='Kaiti', name='subsection', leading=25,borderPadding=(20,0,20,0), fontSize=20,  textColor="#FF5600", wordWrap='CJK'))
styles.add(ParagraphStyle(fontName='Kaiti', name='content', leading=25, fontSize=16, borderPadding=(10,0,0,0), textColor="black", wordWrap='CJK'))
styles.add(ParagraphStyle(fontName='Kaiti', name='xu', leading=25,borderPadding=(20,0,20,0), fontSize=14,  textColor="#9200D0", wordWrap='CJK'))
styles.add(ParagraphStyle(fontName='Kaiti', name='footer', leading=20, fontSize=10, LineIndent=0,alignment=0, wordWrap='CJK'))

class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)

    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'chapter' or style == 'book':
                level = 0
                pageNum = self.page
                key = str(hash(flowable))
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level,closed=1)
            elif style == 'subsection':
                level = 1
                if bridge:
                    level=0
                pageNum = self.page
                key = str(hash(flowable))
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text.replace("○",""), key, level=level,closed=1)
            else:
                return

def doHeading(data, text, sty):
    from hashlib import sha1
    # create bookmarkname
    bn = sha1(text.encode("utf-8")).hexdigest()
    # modify paragraph text to include an anchor point with name bn
    h = Paragraph(text + '<a name="%s"/>' % bn, sty)
    # store the bookmark name on the flowable so afterFlowable can see this
    h._bookmarkName = bn
    data.append(h)

# Page Number
def footer(canvas, doc):
    page_num = canvas.getPageNumber()
    canvas.saveState()
    P = Paragraph("第 %d 頁" % page_num , styles['footer'])
    w, h = P.wrap(doc.width, doc.bottomMargin)
    P.drawOn(canvas, doc.leftMargin + w/2, h)
    canvas.restoreState()

# load txt file
def loadTxt(txt_path):
    with open(txt_path, 'r') as f:
        txt_datas = f.readlines()
    return txt_datas

def toPDF(txt_datas, pdf_path):
    PDF = MyDocTemplate(pdf_path, pagesize=A4)
    frame = Frame(PDF.leftMargin, PDF.bottomMargin, PDF.width, PDF.height, id='normal')
    template = PageTemplate(frames=frame, onPage=footer)
    PDF.addPageTemplates([template])

    data = []

    NUM = 0
    # add txt
    for txt_data in txt_datas:
        txt_data = txt_data.lstrip() # remove left space
        if len(txt_data) == 0: # no text
           data.append(Spacer(10,10))
           NUM = NUM + 1
           continue 

        if txt_data[0] == "○":
            doHeading(data, txt_data, styles['subsection'])
        elif  ("更新日期" in txt_data): 
            data.append(Paragraph(txt_data, styles['content']))
            data.append(PageBreak())
        elif  (re.match('^# ',txt_data)):
            line=txt_data.replace('# ', '')
            book=line.split('|')[0]
            try:
                author=line.split('|')[1]
            except:
                author=""
            doHeading(data, book, styles['book'])
            data.append(Paragraph(author, styles['author']))
            if bridge:
                data.append(PageBreak())
        elif  (re.match('^## ',txt_data)):
            data.append(PageBreak())
            doHeading(data, txt_data.replace('#', '').replace(' ', ''), styles['chapter'])
        elif  (re.match('^(序:|【按語】)',txt_data)):
            data.append(Paragraph(txt_data, styles['xu']))
        else:
            data.append(Paragraph(txt_data, styles['content']))
        NUM = NUM + 1
        #print('{} line'.format(NUM))

    data.append(PageBreak())
    doHeading(data, "獲取最新版本", styles['chapter'])
    data.append(Spacer(20,20))
    data.append(Paragraph('下載最新版本，請訪問: https://github.com/bgc2017/chtxt',styles['content']))
    data.append(Spacer(10,10))
    data.append(Paragraph('如果您發現錯字、脫字、衍字，請反饋至: https://github.com/bgc2017/chtxt/issues',styles['content']))

    PDF.multiBuild(data)
    print(pdf_file)
    print('Done!')

if __name__ == "__main__":
    txt_file=sys.argv[1]
    bridge_book=["宋詞三百首.txt","弟子規.txt","急就章.txt","聲律啟蒙.txt","笠翁對韻.txt","道德經.txt","三十六計.txt"]
    if basename(txt_file) in bridge_book:
        bridge=True
    pdf_file=txt_file.replace("txt","pdf")
    txt_datas = loadTxt(txt_file)
    toPDF(txt_datas, pdf_file)
