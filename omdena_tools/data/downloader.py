from pathlib import Path
import requests
# from sys import stdout
from tempfile import TemporaryDirectory
# from os import makedirs
# from os.path import dirname, exists
# import warnings
import zipfile

from omdena_tools.data import CT_DATA_DIR


_STREAM_CHUNK_SIZE = 32768
_GDRIVE_URL = 'https://docs.google.com/uc?export=download'


class DownloaderError(Exception):
    """Error raised when an error occurs during data download.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class URLDownloader:
    """Class to download shared files from a URL. This is a modified
    version of
    `google-drive-downloader
    https://github.com/ndrplz/google-drive-downloader`_.
    """

    @staticmethod
    def download(url, destination):
        """Downloads a shared file from google drive into a given folder.
        Optionally unzips it.
        Args:
            url (:obj:`str`): The file url.
            destination (:obj:`str`): The destination directory where the
                downloaded data will be saved.
        """

        if destination.exists() and not destination.is_dir():
            raise DownloaderError(
                'Destination directory {} is a pre-existing file.'.format(
                    repr(str(destination))))
        else:
            destination.mkdir(parents=True, exist_ok=True)

        with TemporaryDirectory() as tmp_dir:
            # Download data zip to temporary directory
            try:
                session = requests.Session()
                response = session.get(url, stream=True)

                curr_dl_size = [0]
                tmp_zip_path = Path(tmp_dir, 'data.zip')
                GoogleDriveDownloader._save_content(response,
                                                    tmp_zip_path,
                                                    curr_dl_size)
            except DownloaderError:
                raise DownloaderError(
                    'An error occured while downloading data.')

            # Extract data to destination directory
            try:
                with zipfile.ZipFile(tmp_zip_path, 'r') as zip_fp:
                    zip_fp.extractall(destination)
            except DownloaderError:
                raise DownloaderError(
                    'An error occured while extracting downloaded data.')

    @staticmethod
    def _save_content(response, destination, curr_size):
        with open(destination, 'wb') as fp:
            for chunk in response.iter_content(_STREAM_CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    fp.write(chunk)
                    curr_size[0] += len(chunk)


class GoogleDriveDownloader:
    """Class to download shared files from Google Drive. This is a modified
    version of
    `google-drive-downloader
        https://github.com/ndrplz/google-drive-downloader`_.
    """

    @staticmethod
    def download(file_id, destination):
        """Downloads a shared file from google drive into a given folder.
        Optionally unzips it.
        Args:
            file_id (:obj:`str`): The file identifier.
            destination (:obj:`str`): The destination directory where the
                downloaded data will be saved.
        """

        if destination.exists() and not destination.is_dir():
            raise DownloaderError(
                'Destination directory {} is a pre-existing file.'.format(
                    repr(str(destination))))
        else:
            destination.mkdir(parents=True, exist_ok=True)

        with TemporaryDirectory() as tmp_dir:
            # Download data zip to temporary directory
            try:
                session = requests.Session()
                response = session.get(_GDRIVE_URL, params={'id': file_id},
                                       stream=True)

                token = None
                for key, value in response.cookies.items():
                    if key.startswith('download_warning'):
                        token = value
                        break

                if token:
                    params = {'id': file_id, 'confirm': token}
                    response = session.get(_GDRIVE_URL, params=params,
                                           stream=True)

                curr_dl_size = [0]
                tmp_zip_path = Path(tmp_dir, 'data.zip')
                GoogleDriveDownloader._save_content(response,
                                                    tmp_zip_path,
                                                    curr_dl_size)
            except DownloaderError:
                raise DownloaderError(
                    'An error occured while downloading data.')

            # Extract data to destination directory
            try:
                with zipfile.ZipFile(tmp_zip_path, 'r') as zip_fp:
                    zip_fp.extractall(destination)
            except DownloaderError:
                raise DownloaderError(
                    'An error occured while extracting downloaded data.')

    @staticmethod
    def _save_content(response, destination, curr_size):
        with open(destination, 'wb') as fp:
            for chunk in response.iter_content(_STREAM_CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    fp.write(chunk)
                    curr_size[0] += len(chunk)


class DataDownloader(object):
    """Class for downloading data described by a :obj:`DownloadInfo` object.
    """

    @staticmethod
    def download(dl_info):
        destination = Path(CT_DATA_DIR, dl_info.destination)

        if dl_info.type == 'url':
            URLDownloader.download(dl_info.url, destination)
        elif dl_info.type == 'google-drive':
            GoogleDriveDownloader.download(dl_info.file_id, destination)
        else:
            raise DownloaderError(
                'Invalid download type {}'.format(repr(dl_info.type)))
