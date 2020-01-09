**Recommend an eel store simlilar to your favorite eel store in Python.**

## Description
* get the store names and reviews of all eel restaurants in Fukuoka from tebelog.com

* clean up for getting accurate date

* recommend an eel store simlilar to your favorite

## Requirement
* Windows10
* Python 3.8.0

## Install
Git clone is easiest to install these files:
```
git clone https://github.com/yuuuusuke1997/eel.git
cd eel
```

## Usage
**step1. scraping_eel.py**

1. Add these libraries:
```
$pip install beautifulsoup4
$pip install requests
$pip install urllib3
$pip install pandas
```

2. Run the file in python console:
```
python scraping_eel.py install
```

And then make sure you got csv file

**step2. morphological_analysis_eel.py**

1. Add these libraries:
```
$pip install Janome
$pip install gensim
$pip install pandas
```

2. Run the file in python console:
```
python morphological_analysis_eel.py install
```

And then make sure you got model file

**step3. word2vec_eel.py**

1. Put your favorite eel store name in on line 10:
`kewword = "富松うなぎ屋黒田本店"`

2. Run the file in python console:
```
python word2vec_eel.py install
```

Then you would get 5 stores with high similarity to your input the store
