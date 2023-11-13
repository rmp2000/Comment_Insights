from datetime import datetime
import os
import string

from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, PageTemplate, Frame, Image,Paragraph, Spacer, Table, TableStyle)


class HeaderContent:
    def __init__(self, image_path, text):
        self.image_path = image_path
        self.text = text

    def build(self, canvas, doc):
        # Set the style for the header text
        style = ParagraphStyle(
            name='HeaderTextStyle',
            fontSize=28,  
            textColor=colors.black,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold"  # Set font type to bold
        )

        # Adjust the horizontal position of the image and text to center them
        image = Image(self.image_path, width=1*inch, height=1*inch)
        text_width = 4*inch  # Maximum text width

        header_text = Paragraph(self.text, style)
        header_text.wrap(text_width, doc.topMargin)

        # Add the image to the header
        image.drawOn(canvas, 54, 705)

        # Add the text to the header
        header_text.drawOn(canvas, 162, 746)

import string

def clean_filename(filename):
    # Valid characters in file names
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

    # Replace invalid characters with underscores
    cleaned_filename = ''.join(c if c in valid_chars else '_' for c in filename)
    
    # Replace spaces with underscores
    cleaned_filename = cleaned_filename.replace(' ', '_')
    
    # Remove consecutive underscores
    cleaned_filename = '_'.join(filter(None, cleaned_filename.split('_')))

    return cleaned_filename

# Function to create a word cloud image
def create_wordcloud(index, wordcloud):
    wordcloud_filename = f"wordcloud{index}.png"
    output_folder = "plots/"
    output_path = os.path.join(output_folder, wordcloud_filename)
    wordcloud[index].to_file(output_path)
    wordcloud_pdf = Image(output_path, width=400, height=200)
    return wordcloud_pdf

# Function to create a PDF document
def create_pdf(values, wordcloud, lines):
    date = datetime.now().date()
    pdf_filename = "{}.pdf".format(clean_filename("{} {} {} {}".format(values['name'], values['device'], values['type'], date)))
    final_path = "pdf_files/{}".format(pdf_filename)  # Change this path to desired location
    doc = SimpleDocTemplate(final_path, pagesize=letter)
    
    # Adjust the frame height to reduce the top space
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-0.7*inch, id='normal')

    # Create the header content (image and text)
    image_path = values["icon"]
    header_text = values["name"]
    header_content = HeaderContent(image_path, header_text)

    template = PageTemplate(id='test', frames=frame, onPage=header_content.build)
    doc.addPageTemplates([template])

    elements=[]
    elements.append(Paragraph("General Information", getSampleStyleSheet()['Title']))
    elements.append(Spacer(1, 12))
    
    # Create a table
    if values['price'][0]=="$":
        aux=values['price'][:-3]
    else:
        aux=values['price']
    data = [["Company", values['company']],
            ["Rating", values['rating']],
            ["Downloads", values['downloads']],
            ["Price", aux],
            ["ESRB", values['age']],
            ["Last Update", values['update']
            ]]
    table = Table(data, colWidths=(140, 370), rowHeights=38)
    style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), Color(0, 0, 128)),
            ('TEXTCOLOR', (0, 0), (-1, 0), Color(255, 255, 255)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 17),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('BACKGROUND', (0, 1), (-1, -1), Color(0.9, 0.9, 0.9)),
            ('GRID', (0, 0), (-1, -1), 1, Color(0, 0, 128))
    ])
    table.setStyle(style)

    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Analysis", getSampleStyleSheet()['Title']))
    elements.append(Spacer(1, 12))
    
    # Second table for analysis
    data = [["Comments", values['leng']],
            ["Rating", values['rating_scrape']],
            ["Start Date", values['date0']],
            ["End Date", values['date1']],
            ["Device", values['device']],
            ["Type", values['type']
            ]]
    table = Table(data, colWidths=(140, 370), rowHeights=38)
    style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), Color(0, 0, 128)),
            ('TEXTCOLOR', (0, 0), (-1, 0), Color(255, 255, 255)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 17),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('BACKGROUND', (0, 1), (-1, -1), Color(0.9, 0.9, 0.9)),
            ('GRID', (0, 0), (-1, -1), 1, Color(0, 0, 128))
    ])
    table.setStyle(style)

    elements.append(table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("WordClouds", getSampleStyleSheet()['Title']))
    
    intro= """
     In our analysis of user feedback from the Play Store, we've generated three WordClouds representing word frequency in the comments. Each WordCloud provides unique insights:
    """
    para1="""
        - This WordCloud encompasses all comments, giving a comprehensive view of the most frequently used words across the board.
    """
    para2= """
        - Focusing specifically on comments with lower app ratings, this WordCloud highlights common themes or concerns expressed by users who rated the app poorly.
    """
    para3= """
        - Contrarily, the WordCloud for the highest-rated comments showcases the positive sentiments.
    """
    para4= """
    This graph showcases comment frequency distributed across months, unveiling insights into user engagement trends over time. By depicting the varying comment volumes month by month
    """

    elements.append(Paragraph(intro, getSampleStyleSheet()['BodyText']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("1. Overall WordCloud:", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph(para1, getSampleStyleSheet()['BodyText']))
    elements.append(Spacer(1, 12))

    elements.append(create_wordcloud(0,wordcloud))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("2. Lowest-Rated Comments WordCloud:", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph(para2, getSampleStyleSheet()['BodyText']))
    elements.append(Spacer(1, 12))
    elements.append(create_wordcloud(1,wordcloud))

    elements.append(Paragraph("3. Highest-Rated Comments WordCloud:", getSampleStyleSheet()['Heading2']))
    elements.append(Paragraph(para3, getSampleStyleSheet()['BodyText']))
    elements.append(Spacer(1, 5))
    elements.append(create_wordcloud(2,wordcloud))
    
    elements.append(Paragraph("Monthly Comment Activity Overview", getSampleStyleSheet()['Title']))
    elements.append(Paragraph(para4, getSampleStyleSheet()['BodyText']))
    image3 = Image(lines, width=590, height=337)
    elements.append(image3)

    
    doc.build(elements)
