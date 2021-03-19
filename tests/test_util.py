from csvw.dsv import reader

from pytular.util import *


def test_fetch_sheet(mocker, tmp_path):
    class Worksheet:
        @property
        def title(self):
            return 'languages'

        def get_all_values(self):
            return [['id', 'name'], ['l1', 'Language 1']]

    class Sheet:
        def worksheets(self):
            return [Worksheet()]

    class Client:
        def open_by_key(self, *args):
            return Sheet()

    mocker.patch('pytular.util.ServiceAccountCredentials', mocker.Mock())
    mocker.patch('pytular.util.gspread', mocker.Mock(authorize=lambda *args: Client()))
    fetch_sheet('languages', keyfile=__file__, output=tmp_path / 'l.tsv')
    assert next(reader(tmp_path / 'l.tsv', delimiter='\t', dicts=True))['name'] == 'Language 1'
