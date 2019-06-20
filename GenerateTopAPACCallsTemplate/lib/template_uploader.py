# coding: utf-8

import sys
import os
sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import resources.email_templates as email_templates

def _get_template_values(template_id, title, subject, body):
	values = [
		('templateId', template_id),
		('type', 'CLIENT'),
		('language', 'en'),
		('purpose', 'GENERALCLIENTMGT'),
		('title', title),
		('subject', subject),
		('body', body)
	]
	return values


def _upload_template(html_template, subject):
	template_id = '1834'
	title = 'Top Transcripts - CN'
	body = html_template
	values = _get_template_values(template_id, title, subject, body)

	email_templates.modify("subject:" + subject, values)


def upload(html_template, subject, region):
	if region.lower() == 'cn':
		_upload_template(html_template, subject)
	else:
		print('Template failed to upload. Region {%s} not found.' % region)
