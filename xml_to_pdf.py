from lxml import etree, objectify

import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

# Change the channel's name here
channelName = 'bogeunchoi'

class PDFOrder(object):
    def __init__(self, xml_file, pdf_file):
        self.xml_file = xml_file
        self.pdf_file = pdf_file

        self.xml_obj = self.getXMLObject()

    def coord(self, x, y, unit=1):
        x, y = x * unit, self.height - y * unit
        return x, y

    def createPDF(self):
        xml = self.xml_obj
        styles = getSampleStyleSheet()
        styles = styles['BodyText']
        styles.wordWrap = 'CJK'

        # Example user
        users = {'U00000000': 'bogeunchoi'}

        data = []
        data.append(['Channel: ' + channelName])
        data.append(["User", "Time", "Message (top = newest)"])

        for item in xml.data.iterchildren():
            # Creating name column
            row = []
            row.append(item.name)

            # Creating time column
            s = item.time
            date = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
            row.append(date)

            # Creating message column
            if ('&#8217;' in item.message.text):
                item.message.text = item.message.text.replace('&#8217;', '\'')

            text = item.message.text

            # Filtering out the @U0... and replacing with usernames
            for key, value in users.items():
                keyPlus = key + '|'
                if keyPlus in text:
                    text = text.replace(keyPlus, "")
                elif key in text:
                    text = text.replace(key, value)

            text = filter(lambda c: c not in "<>", text)

            message = Paragraph(text, styles)
            row.append(message)

            data.append(row)

        t = Table(data, colWidths=(75, 110, 100*mm), hAlign='CENTER')
        t.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (0, 0), (-1, 0))
        ]))
        width, height = t.wrap(0, 0)
        w = width
        h = height

        self.canvas = canvas.Canvas(self.pdf_file, pagesize=(w, h))
        width, self.height = letter

        t.wrapOn(self.canvas, width, self.height)
        t.drawOn(self.canvas, 0, 0)
        t.canvas = self.canvas

    def getXMLObject(self):
        with open(self.xml_file) as f:
            xml = f.read()
        return objectify.fromstring(xml)

    def savePDF(self):
        self.canvas.save()

if __name__ == "__main__":
    # Change the name of the xml file you want to get data from
    xml = channelName + 'Data.xml'
    # Change the name of the pdf file you want to create
    pdf = channelName + 'Data.pdf'
    doc = PDFOrder(xml, pdf)
    doc.createPDF()
    doc.savePDF()
    print('PDF Created')