import os
import json
from pathlib import Path
import unittest
from unittest.mock import patch, mock_open
from utils import create_or_edit_file, backup_file, check_and_restore_important_file

class TestUnitFunctions(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_create_or_edit_file(self, mock_file):
        filename = 'test_file.json'
        content = {'key': 'value'}
        
        mock_file.side_effect = [mock_open(read_data=json.dumps({"directory": ""}))]

        create_or_edit_file(filename, content)
        path = os.path.join(str(Path.cwd()), "room") 
        mock_file.assert_called_once_with(os.path.join(path, filename), 'w')

    @patch('os.makedirs')
    @patch('shutil.copy')
    def test_backup_file(self, mock_copy, mock_makedirs):
        filename = 'test_file.txt'
        backup_file(filename)
        
        mock_makedirs.assert_called_once_with(os.path.join(os.getcwd(), "backups"), exist_ok=True)  # إضافة exist_ok=True
        mock_copy.assert_called_once_with(filename, os.path.join(os.getcwd(), "backups", filename))


    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False) 
    def test_check_and_restore_important_file(self, mock_exists, mock_open):
        default_content = {'key': 'value'}
        path = os.path.join(str(Path.cwd()), "room") 
        filename = os.path.join(path, "important_file.json")
        check_and_restore_important_file(filename, default_content)

        mock_open.assert_called_once_with(filename, 'w')

        mock_open().write.assert_called_once_with(json.dumps(default_content))

if __name__ == '__main__':
    unittest.main()
