import csv
import os


class CsvAccesser():
    base_dir = ''
    csv_dir = '/scripts/csv'
    ext_style_path = '/path/to/example.csv'
    fieldnames = []  # list of csv header

    def __init__(self, base_dir, fileName, fieldnames) -> None:
        self.base_dir = base_dir.replace(os.path.sep, '/')
        self.ext_style_path = self.csv_dir + '/' + fileName
        self.fieldnames = fieldnames

    def get_csv_path(self):
        p = self.base_dir + self.ext_style_path
        return p

    def read_csv_without_header(self):
        path = self.get_csv_path()
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def append_to_csv(self, row):
        with open(self.get_csv_path(), 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(row)

    def delete_from_csv(self, id):
        rows = self.read_csv_without_header()
        with open(self.get_csv_path(), 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for row in rows:
                if row['id'] != id:
                    writer.writerow(row)
