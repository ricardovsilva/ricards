# RiCARDS - Issuer basic card authorization and billing system
RiCARDS is a challenge to a python software engineer position. It is a really good example of how to use Django to create RestAPIs with Djangorestframework.

This application is basically an API that will receive some transactions (both autorisation and presentment) and do some processing. As Issuer, the system needs to communicate with other players of digital payment process. This example don't cover that communications, so I choose to simple stub that players.

## Requirements
This system is developed using Python 3.6. So, in order to run that, Python 3.6 is mandatory. For this challenge I'm using sqlite3, which for demonstration purpose is excelent. But don't use this at a production environment. Into production environment you will probably need a more robust database like Postgresql or MySql.

## Cloning and running
1. Clone this repository
2. Change directory to where you downloaded it:
> $ cd ~/git/ricards
3. Install all external modules, including django:
> $ pip install -r requirements.txt
4. Create database and run migrations:
> $ ./manage.py migrate
5. Run all tests to ensure that you doesn't have downloaded a broken version:
> $ ./manage.py test
6. Run server
> $ ./manage.py runserver

After that you will be allowed to perform RESTful operations to the API.

## Usage
### Endpoints 
By now, the API has only one endpoint to post new transactions (authorisation and presentment).
You can post a transaction to /transaction. Below are examples of authorisation and presentment jsons (all fields are mandatory):
```json
  {  
    "type":"authorisation",
    "card_id":"4321LOBO",
    "transaction_id":"1234ZORRO",
    "merchant_name":"SNEAKERS​ ​ R ​ ​ US",
    "merchant_country":"US",
    "merchant_mcc":"5139",
    "billing_amount":"90.00",
    "billing_currency":"EUR",
    "transaction_amount":"100.00",
    "transaction_currency":"USD"
  }
```

```json
  {
    "type": "presentment",
    "card_id": "4321LOBO",
    "transaction_id": "1234ZORRO",
    "merchant_name": "SNEAKERS    R     US",
    "merchant_city": "LOS    ANGELES",
    "merchant_country": "US",
    "merchant_mcc": "5139",
    "billing_amount": "91.00",
    "billing_currency": "EUR",
    "transaction_amount": "100.00",
    "transaction_currency": "USD",
    "settlement_amount": "90.50",
    "settlement_currency": "EUR"
  }
```
### Commands
Is possible to load money to some account by console line. To do that follow the steps below:
1. Navigate to root of project
> $ cd ~/git/ricards
2. Run management.py with load_money with the parameters below:
> $ ./management.py load_money [card_id] [amount] [currency]

## The basic architecture and strategy approached
I tried to keep things separated as much as possible without kill the simplicity. So some things are in same file, for example models. As system grow, it highly recommended that models moves from one file to their own file.
Also I applied the service pattern because I want to keep my Views (or Controllers to people that is more accustomed with MVC pattern) as much anemic as possible and move the domain rules to model classes, and integration between that classes in services.
Services in that example are POCO classes, but it allows to easily move to a microarchitecture in future.

## TDD
I'm totally adept of TDD. For me is strange develop without TDD and I try to test as many things I can. I tried to make my tests really unit tests. I dislike the approach of Django (and also the Rails aproach) to setup a test database and mock some data into that database to do some things. In my opinion, this is a bad point because I have to run migrations before test.
If you take a look at tests, you will see that I mocked or stubed everything, no database would be required to test if it was not a Django particularity (if you know how to disable all dependencies to database when running tests, please let me know).

## About technology used
I believe that Django is a really great tool to web development and it has a concept, of solution with applications. But, since that example is really simple and has a few endpoints, for me Django is an overkill for that solution.
I'm doing this challenge with Django because it was a requirement, but to a production, new system, I would prefer to go to Pyramid or Flask (if I want to keep that in python) or to Ruby + Sinatra.
I believe that Ruby + Sinatra is more adequated to that problem because of it's simplicity and development speed to create api's with a few endpoints.

## What is already developed?
This problem has 3 main points to attack, so I'm trying to do that with baby steps. They are:

- [x] Account value management and authorization and money reservation
- [x] Transaction history to make presentment and effectivelly remove money from account
- [x] Transfer of money to other stakeholders in digital payment system
- [x] Create management command to load money into customer account

## Observations
- This repository is highly opinated base;
- A lot of things that I said is based on my professional experience and a lot of research. It is not absolute truth;
- Probably are better solutions than this, and, if for some reason no one developed or draw a better solution (wich I really doubt), this solution can be highly improved with more developers and more minds involved;
- If you have any suggestion, question, bugfix. Please, feel free to open an issue or a pull request.
- I'm trying to improve my own development habilities and also help other developers, if you have some time, take a look at this repository https://github.com/ricardovsilva/good-programming-practices and help-me improve that.
