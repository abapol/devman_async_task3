# Microservice for downloading files

The microservice helps the work of the main site made on CMS and serves requests for downloading archives with files. A microservice can do nothing but pack files into an archive.

Creating an archive occurs on the fly upon request from the user. The archive is not saved to disk, instead, as it is packed, it is immediately sent to the user for downloading.


## How to install

For the microservice to work, you need Python version 3.6 and higter.

```bash
pip install -r requirements.txt
```


## How to start

```bash
python server.py
```

The server will start on port 8080, to check its operation, go to the browser on the page http://0.0.0.0:8080/.


## Arguments

You can use this arguments:

--log : For activate debug-mode of logging

--delay : For set delay of response in seconds

--folder : To set your directory with foto-files

Example:

```bash
python server.py --log --delay=0.5 --folder='images/'
```

