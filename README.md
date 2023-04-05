# Screenshot Classifier

Image classifier that detects valorant screenshots.


# Setup

1. Install `mamba`
2. Create an environment `mamba env create -n sc --file src/requirements.txt`
3. Activate `mamba activate sc`
4. Install extra dependencies (if you want to use the scraper)
    - `pip install streamlink`
5. Put `val-detect.py` on your `$PATH`


# CLI usage

Run `val-detect <path_to_model.pkl> <path_to_image.png|jpg|etc>`

