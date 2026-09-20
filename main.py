from virtual_library.settings import load_settings
from virtual_library.ui import BookDownloaderApp


def main() -> None:
    load_settings()
    BookDownloaderApp().run()


if __name__ == "__main__":
    main()
