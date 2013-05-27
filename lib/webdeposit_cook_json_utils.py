# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.


"""
Cook Json Functions

Functions to be used in for transforming a webdeposit json
(json representing a form) to rec json format using BibField's JsonReader
"""


def cook_title(json_reader, title):
    json_reader['title.title'] = title
    return json_reader


def cook_subtitle(json_reader, subtitle):
    json_reader['title.subtitle'] = subtitle
    return json_reader


def cook_publisher_name(json_reader, publisher):
    json_reader['imprint.publisher_name'] = publisher
    return json_reader


def cook_date(json_reader, date):
    json_reader['imprint.date'] = date
    return json_reader


def cook_language(json_reader, language):
    json_reader['language'] = language
    return json_reader


def cook_publication_title(json_reader, title):
    json_reader['publication_info.title'] = title
    return json_reader


def cook_issn(json_reader, issn):
    json_reader['issn'] = issn
    return json_reader


def uncook_files(webdeposit_json, recid=None, json_reader=None):
    if 'files' not in webdeposit_json:
        webdeposit_json['files'] = []

    if recid is None:
        for f in json_reader['url']:
            filename = f['url'].split('/')[-1]
            file_json = {
                'name': filename
            }
            webdeposit_json['files'].append(file_json)

    else:
        for f in BibRecDocs(recid, human_readable=True).list_latest_files():
            filename = f.get_full_name()
            path = f.get_path()
            size = f.get_size()
            file_json = {
                'name': filename,
                'file': path,
                'size': size
            }
            webdeposit_json['files'].append(file_json)

    return webdeposit_json


def cook_icon(json_reader, icon_path):
    """ helper for adding an icon to a deposition
        e.g. Photo deposition """
    try:
        json_reader['fft[-1]']['icon_path'] = icon_path
    except IndexError:
        pass
    return json_reader


def cook_publication_doi(json_reader, doi):
    json_reader['publication_info.DOI'] = doi
    return json_reader


def cook_url(json_reader, url):
    json_reader['url[0].url'] = url
    return json_reader


def cook_first_authors_full_name(json_reader, full_name):
    json_reader['authors[0].full_name'] = full_name
    return json_reader


def cook_abstract_summary(json_reader, summary):
    json_reader['abstract.summary'] = summary
    return json_reader


def cook_record_id(json_reader, recid):
    json_reader['recid'] = recid
    return json_reader


def cook_comment(json_reader, comment):
    json_reader['comment'] = comment
    return json_reader


""" Cooks for the deposition files """


def cook_files(json_reader, file_list):
    """ @param file_json: list (as created in blueprints)
                          containing dictionaries with files and their metadata
    """

    for file_json in file_list:
        filename = file_json['name']
        path = file_json['file']

        json_reader['fft[n]'] = {'path': path,
                                 'new_name': filename}
    return json_reader


def cook_icon(json_reader, icon_path):
    """ helper for adding an icon to a deposition
        e.g. Photo deposition """
    try:
        json_reader['fft[-1]']['icon_path'] = icon_path
    except IndexError:
        pass
    return json_reader


def cook_picture(json_reader, file_list):
    """ Same as file cook with an additional icon cook
        It is assumed that its used for depositing one picture
    """

    if len(file_list) == 1:
        json_reader = cook_files(json_reader, file_list)
        json_reader = cook_icon(json_reader, file_list[0]['file'])

    return json_reader
