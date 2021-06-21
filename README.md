# REST API With Flask & SQL Alchemy

> Coupons API for discount code management

## Quick Start Using Pipenv

``` bash
# Activate venv
$ pipenv shell

# Install dependencies
$ pipenv install

# Create DB
$ python
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhst:5000)
python app.py
```

## ADMIN Endpoints for Brands

* POST    /admin/:brand_id/coupons/create/:coupon_count
* GET     /admin/:brand_id/coupons
* GET     /admin/:brand_id/coupon/:id
* PUT     /admin/:brand_id/coupon/:id/:coupon_status
* DELETE  /admin/:brand_id/coupon/:id

## USER Endpoints for customers
/user/:customer_id/discount_code
