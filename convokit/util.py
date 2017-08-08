import urllib.request
import shutil
import os
import pkg_resources

# returns a path to the dataset file
def download(name, verbose=True):
    """Use this to download (or use saved) convokit data by name.

    :param name: Which item to download. Currently supported:

        - "wiki-corpus": Wikipedia Talk Page Conversations Corpus (see
            http://www.cs.cornell.edu/~cristian/Echoes_of_power.html)
        - "supreme-corpus": Supreme Court Dialogs Corpus (see
            http://www.cs.cornell.edu/~cristian/Echoes_of_power.html)

    :return: The path to the downloaded item.
    """
    DatasetURLs = {
        "wiki-corpus": "http://zissou.infosci.cornell.edu/socialkit/" + \
            "datasets/wiki-corpus/full.json",
        "supreme-corpus": "http://zissou.infosci.cornell.edu/socialkit/" + \
            "datasets/supreme-corpus/full.json"
    }
    name = name.lower()
    data_dir = pkg_resources.resource_filename("convokit", "")
    dataset_path = os.path.join(data_dir, "downloads", name)
    if not os.path.exists(os.path.dirname(dataset_path)):
        os.makedirs(os.path.dirname(dataset_path))

    downloadeds_path = os.path.join(data_dir, "downloads", "downloaded.txt")
    if not os.path.isfile(downloadeds_path):
        open(downloadeds_path, "w").close()
    with open(downloadeds_path, "r") as f:
        downloaded = f.read().splitlines()

    if name not in downloaded:
        url = DatasetURLs[name]
        with urllib.request.urlopen(url) as response, \
                open(dataset_path, "wb") as out_file:
            if verbose:
                l = float(response.info()["Content-Length"])
                length = str(round(l / 1e6, 1)) + "MB" \
                        if l > 1e6 else \
                        str(round(l / 1e3, 1)) + "KB"
                print("Downloading", name, "from", url,
                        "(" + length + ")...", end=" ")
            shutil.copyfileobj(response, out_file)
            if verbose:
                print("Done")
        with open(downloadeds_path, "a") as f:
            f.write(name + "\n")
    return dataset_path

