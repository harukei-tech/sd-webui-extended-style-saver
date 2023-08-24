from ..lib.csv_accesser import CsvAccesser


class ExtStyles():
    whole_styles: list
    csvAccesser: CsvAccesser

    def __init__(self, basedir) -> None:
        self.csvAccesser = CsvAccesser(basedir)
        self.refresh()

    def refresh(self):
        self.whole_styles = self.csvAccesser.read_csv_without_header()

    def create_choice_name(self, style):
        split = '.'
        m_idx = style["sd_model_checkpoint"].rfind(split)
        model_name = style["sd_model_checkpoint"][:m_idx]
        v_idx = style["sd_vae"].rfind(split)
        vae_name = style["sd_vae"][:v_idx]

        return style['name'] + f'({model_name}, {vae_name})'

    def get_choices(self, styles=None):
        if styles is None:
            styles = self.whole_styles
        return [self.create_choice_name(style) for style in styles]

    def get_contents(self):
        return self.whole_styles

    def get_content(self, index):
        return self.whole_styles[index]

    def save(self, row):
        self.csvAccesser.append_to_csv(row)
        self.refresh()


def log(text: str):
    print(f"[Externded Styles] {text}")
