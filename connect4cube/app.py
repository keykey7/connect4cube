class App:
    def run(self):
        raise NotImplementedError

    def get_preview(self):
        raise NotImplementedError

    def get_description(self) -> str:
        raise NotImplementedError
