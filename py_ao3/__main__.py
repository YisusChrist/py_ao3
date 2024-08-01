from rich.traceback import install

from py_ao3.ui import AO3ReportApp


def main() -> None:
    install()
    app = AO3ReportApp()
    app.run()


if __name__ == "__main__":
    main()
