# coding: utf-8

import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor


sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import resources.tools as tools
import resources.intranet as intranet
import resources.misc_report_data as misc_report_data
import resources.setup as setup_mod

import GenerateTopAPACCallsTemplate.lib.google_api_mod as google_api_mod
import GenerateTopAPACCallsTemplate.lib.template_uploader as template_uploader


def set_html_template():
    global html_template
    html_template = tools.read_file('templates/main_template.html')


def update_html_template(old_str, new_str):
    global html_template
    html_template = html_template.replace(old_str, new_str)


def replace_month():
    month = setup.get('Month')
    update_html_template('$month', month)


def replace_year():
    year = setup.get('Year')
    update_html_template('$year', year)


def replace_stats():
    telephones = setup.get('Telephones')
    update_html_template('$telephones', telephones)
    conferences = setup.get('Conferences')
    update_html_template('$conferences', conferences)


def replace_month_and_year():
    replace_month()
    replace_year()
    replace_stats()


def validate_fields():
    required_fields = [
        'Month',
        'Year'
    ]
    setup.validate_values(required_fields)


def load_setup_file():
    global setup
    setup = setup_mod.Setup('Setup.txt')
    validate_fields()


def _add_event_details_to_dict(intranet_dict, section):
    for i in range(len(section)):
        for d in intranet_dict:
            if d['e_id'] == section[i][0]:
                section[i].append(d['e_uuid'])
    return section


def _get_intranet_data(section_data):
    event_ids = [events[0] for events in section_data]
    cc_str = '%2C'.join(map(str, event_ids))
    id_and_params = "1059&ConferenceCallID=%s" % (cc_str)
    results = misc_report_data.get_dict_list(id_and_params)

    return results


def _section_processing(section):
    intranet_data = _get_intranet_data(section)
    new_section = _add_event_details_to_dict(intranet_data, section)
    return new_section


def update_section(section_data, section_html):
    section_string = ''
    for data in section_data:
        section_row = tools.read_file('templates/{section_html}.html')
        section_row = section_row.replace('$event_title', data[1])
        section_row = section_row.replace('$sector_field', data[2])
        section_row = section_row.replace('$specialist_title', data[3])
        section_row = section_row.replace('$event_uuid', data[4])
        section_string += section_row

    update_html_template('${section_html}', section_string)


def set_template_and_parse_data(blue, red, yellow):
    set_html_template()
    replace_month_and_year()

    print('China count: {}'.format(len(blue)))
    print('Asia count: {}'.format(len(red)))
    print('Global count: {}'.format(len(yellow)))

    update_section(blue, 'section_1')
    update_section(red, 'section_2')
    update_section(yellow, 'section_3')


def get_template_data():
    with ThreadPoolExecutor(max_workers=3) as pool:
        t1 = pool.submit(google_api_mod._parse_source, 'China')
        t2 = pool.submit(google_api_mod._parse_source, 'Asia')
        t3 = pool.submit(google_api_mod._parse_source, 'Global')

        blue = t1.result()
        red = t2.result()
        yellow = t3.result()

        # remove headers
        del blue[0]
        del red[0]
        del yellow[0]

        blue = _section_processing(blue)
        red = _section_processing(red)
        yellow = _section_processing(yellow)

        return blue, red, yellow


def main():

    intranet.login()
    load_setup_file()
    month = setup.get('Month')
    region=setup.get('Region')
    subject=setup.get('Subject')

    blue, red, yellow = get_template_data()
    set_template_and_parse_data(blue, red, yellow)

    output_html_name = ('Top_APAC_Transcripts_-_{}.html').format(month)
    tools.write_to_file(output_html_name, html_template)

    template_uploader.upload(html_template, subject, region)

    print('Done')


if __name__ == '__main__':
    main()
