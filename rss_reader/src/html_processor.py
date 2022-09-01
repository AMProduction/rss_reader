#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
from . import file_processing_utilities, utilities
from .rss_reader_errors import SaveToHTMLError

news_html_folder = 'news_html'


def save_data_to_html(input_dict: dict, limit: int) -> None:
    final_html = '''
    <html>
        <body>
            <h1>
    '''
    final_html += input_dict['Blog title'] + '</h1>'
    final_html += '<h2><a href="' + input_dict['Blog link'] + '">' + input_dict['Blog link'] + '</a></h2><hr>'
    limit_counter = 0
    for post in input_dict['posts']:
        final_html += '<p><h3>' + post['title'] + '</h2>'
        final_html += utilities.get_formatted_date_to_pdf(post['date']) + '<br>'
        final_html += '<a href="' + post['link'] + '">' + post['link'] + '</a><br>'
        for link in post['links']:
            if link.endswith('.jpg'):
                final_html += '<img src="' + link + '">'
        final_html += '</p><hr>'
        limit_counter += 1
        if limit != 0 and limit_counter == limit:
            break
    final_html += '''            
        </body>
    </html>
    '''

    try:
        if not file_processing_utilities.is_dir_exists(news_html_folder):
            file_processing_utilities.create_news_folder(news_html_folder)
        file_name = file_processing_utilities.get_file_name(news_html_folder, input_dict, '.html')
        with open(file_name, 'w', encoding='utf-8') as html_file:
            html_file.write(final_html)
    except OSError:
        raise SaveToHTMLError
