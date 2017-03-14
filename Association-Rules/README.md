# Association-Rules
Wiki: https://en.wikipedia.org/wiki/Association_rule_learning
Virtualenv used for the development.

## Features
* `support` operation

## Clone
```
git clone https://github.com/sokaRepo/Data-Mining/tree/master/Association-Rules
```

## Install dependencies
Under virtualenv
```
(venv) pip install -r requirements.txt
```
Without
```
(sudo) pip install -r requirements.txt
```

## Usage 
```
Usage: python app.py operation ingredients
Examp: python app.py support "beef,wine"
```

## Output
```
Meals available :
hamburger
	beef
	tomato
	salad
	bread
chilly con carne
	chilly
	beef
	bean
curry chicken
	chicken
	curry
	fresh cream
coco chicken
	coconut milk
	chiken
crepes
	milk
	sugar
	flour
beuf bourgigon
	beef
	wine
	carrot
----------------------------
supp({beef,wine}) = 1/6
```