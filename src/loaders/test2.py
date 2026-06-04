from loaders.rbi_payment_indicator_downloader import (
    download_new_files
)

files = download_new_files()

print(files)