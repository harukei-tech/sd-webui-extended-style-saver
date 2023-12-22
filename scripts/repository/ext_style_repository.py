from ..lib.csv_accesser import CsvAccesser


class ExtStyleRepository():
    whole_styles: list
    csvAccesser: CsvAccesser
    fileName = 'ext_style.csv'
    fieldnames = ['id', 'name', 'sd_model_checkpoint', 'sd_vae',
                  'prompt', 'negative_prompt', 'width', 'height']

    def __init__(self, basedir) -> None:
        self.csvAccesser = CsvAccesser(
            basedir, fileName=self.fileName, fieldnames=self.fieldnames)
        self.refresh()

    def refresh(self):
        self.whole_styles = self.csvAccesser.read_csv_without_header()

    # for dropdown menu.
    def create_choice_name(self, style):
        # split = '.'
        # m_idx = style["sd_model_checkpoint"].rfind(split)
        # model_name = style["sd_model_checkpoint"][:m_idx]
        # v_idx = style["sd_vae"].rfind(split)
        # vae_name = style["sd_vae"][:v_idx]

        model_name = style["sd_model_checkpoint"]
        vae_name = style["sd_vae"]
        id = style["id"]

        return style['name'] + f'({model_name}, {vae_name}, {id})'

    def get_choices(self, styles=None):
        self.refresh()  # to avoid data rollback by F5 reload
        if styles is None:
            styles = self.whole_styles
        return [self.create_choice_name(style) for style in styles]

    def get_contents(self):
        self.refresh()  # to avoid data rollback by F5 reload
        return self.whole_styles

    def get_content(self, choice_name):
        self.refresh()
        return next(filter(lambda style: self.create_choice_name(style) == choice_name, self.whole_styles), None)

    def save(self, row):
        self.csvAccesser.append_to_csv(row)
        self.refresh()

    def delete(self, id):
        self.csvAccesser.delete_from_csv(id)
        self.refresh()
