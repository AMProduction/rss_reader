#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
from fpdf import FPDF

from . import file_processing_utilities, utilities
from .rss_reader_errors import SaveToPDFError

news_pdf_folder = 'news_pdf'


class PDF(FPDF):
    """
    Base set up the PDF
    """
    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def save_dict_to_pdf(input_dict: dict, limit: int) -> None:
    """
    Save RSS feed topics to PDF file

    :param input_dict: a formatted dictionary of RSS feed topics
    :param limit: If `--limit` is not specified or `--limit` is larger than feed size then user should get all available news
    :return: None
    """
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.add_font('DejaVu', fname='DejaVuSansCondensed.ttf')
    pdf.set_font("DejaVu", size=20)
    pdf.write(txt=input_dict['Blog title'])
    pdf.set_font(style="U")
    link = pdf.add_link()
    pdf.write(10, input_dict['Blog link'], link)
    limit_counter = 0
    for post in input_dict['posts']:
        pdf.set_font("DejaVu", size=12)
        pdf.ln(10)
        pdf.write(10, txt="********************************************************************")
        pdf.ln(10)
        pdf.write(10, txt=post['title'])
        pdf.ln(10)
        formatted_date = utilities.get_formatted_date_to_pdf(post['date'])
        pdf.write(10, txt=formatted_date)
        pdf.ln(10)
        pdf.set_font(style="U")
        pdf.cell(txt=post['link'], link=post['link'])
        for link in post['links']:
            if link.endswith('.jpg'):
                pdf.ln(10)
                pdf.image(link, w=pdf.epw / 3)
        limit_counter += 1
        if limit != 0 and limit_counter == limit:
            break

    try:
        if not file_processing_utilities.is_dir_exists(news_pdf_folder):
            file_processing_utilities.create_news_folder(news_pdf_folder)
        file_name = file_processing_utilities.get_file_name(news_pdf_folder, input_dict, '.pdf')
        pdf.output(file_name)
    except OSError:
        raise SaveToPDFError
