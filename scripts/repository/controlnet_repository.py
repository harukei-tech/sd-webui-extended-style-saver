from ..lib.csv_accesser import CsvAccesser


class ControlnetRepository():
    whole_styles: list
    csvAccesser: CsvAccesser
    fileName = 'controlnet.csv'
    fieldnames = ['id', 'extended_style_id', 'model',
                  'image', ]

    def __init__(self, basedir) -> None:
        self.csvAccesser = CsvAccesser(
            basedir, fileName=self.fileName, fieldnames=self.fieldnames)
        self.refresh()

    def refresh(self):
        self.whole_styles = self.csvAccesser.read_csv_without_header()

    def save(self, row):
        self.csvAccesser.append_to_csv(row)

    def get_contents(self, extended_style_id):
        self.refresh()  # to avoid data rollback by F5 reload
        return [record for record in self.whole_styles if record['extended_style_id'] == extended_style_id]

    def get_image_name(self, row):
        return row['image']
