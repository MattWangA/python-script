# coding: utf-8

LANGUAGES_LIST = '''
select DISTINCT Label as LongName, Subfield as ShortName from cognoweb.strings where Field='Language' and Subfield<>'' and Language in ('en','*') order by LongName ASC
'''