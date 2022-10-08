
# Posts Facebook Scraper

This small library provides tools to scape posts on facebook and them on MongoBD.

## Installation

### Step 1: Create a new conda environment

```bash
conda create -m env_name python==3.8
```

### Step 2: Activate the environment

On linux

```bash
source env_name/bin/activate
```

On Windows

```bash
activate env_name
```

### Step 3: Download chromedriver accoring your os

Download link [chrome driver](https://chromedriver.chromium.org/downloads). 

### Step 4: Install dependancies in your environment

Use the following command to install all requirements.

```bash
pip install -r requirements.txt
```


### Step 6: Provide downloaded chromedriver path in .env file

-Open .env file and find "CHROME_DRIVER_PATH" .
example : CHROME_DRIVER_PATH="C:\\Users\\tabou\\Desktop\\smart\\resources\\chromedriver.exe"


## Usage

To start scrapping type python main.py -h and see arguments.

```python
python main.py --email "53491126" --password "abcdeda" -t "iphone" --erase_exist False
```

Watch printing in terminal

## License

[MIT](https://choosealicense.com/licenses/mit/)