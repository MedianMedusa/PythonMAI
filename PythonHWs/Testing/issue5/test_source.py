import source
import pytest
from unittest.mock import MagicMock, patch


@patch('urllib.request.urlopen')
def test_yyyymmdd(mock):
    mock_template = MagicMock()
    mock_template.getcode.return_value = 200
    mock_template.read.return_value = \
        '{"currentDateTime":"2021-00-00T02:28Z"}'
    mock_template.__enter__.return_value = mock_template
    mock.return_value = mock_template

    year = source.what_year_is_it()
    assert year == 2021


@patch('urllib.request.urlopen')
def test_ddmmyyyy(mock):
    mock_template = MagicMock()
    mock_template.getcode.return_value = 200
    mock_template.read.return_value = \
        '{"currentDateTime":"00.00.2021T13:37Z"}'
    mock_template.__enter__.return_value = mock_template
    mock.return_value = mock_template

    year = source.what_year_is_it()
    assert year == 2021


@patch('urllib.request.urlopen')
def test_slash(mock):
    mock_template = MagicMock()
    mock_template.getcode.return_value = 200
    mock_template.read.return_value = \
        '{"currentDateTime":"00/00/2021T16:20Z"}'
    mock_template.__enter__.return_value = mock_template
    mock.return_value = mock_template

    with pytest.raises(ValueError):
        source.what_year_is_it()
