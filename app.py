from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

from datetime import datetime
from random_string import create_random_coupon

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Coupon Class/Model
class Coupon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  coupon_string = db.Column(db.String(50), unique=True)
  coupon_status = db.Column(db.String(10))
  discount = db.Column(db.Float)
  coupon_user_id = db.Column(db.Integer)
  brand_id = db.Column(db.Integer)
  coupon_group = db.Column(db.String(50))
  created_at = db.Column(db.String(50))
  modified_at = db.Column(db.String(50))

  def __init__(self, coupon_string, coupon_status, discount, coupon_user_id, brand_id, coupon_group, created_at, modified_at):
    self.coupon_string = coupon_string
    self.coupon_status = coupon_status
    self.discount = discount
    self.coupon_user_id = coupon_user_id
    self.brand_id = brand_id
    self.coupon_group = coupon_group
    self.created_at = created_at
    self.modified_at = modified_at

# Coupon Schema
class CouponSchema(ma.Schema):
  class Meta:
    fields = ('id', 'coupon_string', 'coupon_status', 'discount', 'coupon_user_id', 'brand_id', 'coupon_group', 'created_at', 'modified_at')

# Init schema
coupon_schema = CouponSchema()
coupons_schema = CouponSchema(many=True)

# ADMIN Endpoints
# Create Coupons
@app.route('/admin/<brand_id>/coupons/create/<coupon_count>', methods=['POST'])
def add_coupons(brand_id, coupon_count):

  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  no_of_coupons = int(coupon_count)
  try:
    discount_value = float(request.json['discount'])
  except:
    discount_value = 2.0 # Default discount 2.0 percent
  for item in range(no_of_coupons):
    coupon_string = create_random_coupon()
    coupon_status = "New"
    discount = discount_value
    coupon_user_id = 0
    brand_id = int(brand_id)
    coupon_group = 'Group_'+ dt_string
    created_at = dt_string
    modified_at = dt_string
    new_coupon = Coupon(coupon_string, coupon_status, discount, coupon_user_id, brand_id, coupon_group, created_at, modified_at)
    db.session.add(new_coupon)
  db.session.commit()

  all_coupons = Coupon.query.all()
  result = coupons_schema.dump(all_coupons)
  return jsonify(result)

# Get All Coupons
@app.route('/admin/<brand_id>/coupons', methods=['GET'])
def get_coupons(brand_id):
  all_coupons = Coupon.query.all()
  initial_result = coupons_schema.dump(all_coupons)
  result = []
  for item in initial_result:
    if item["brand_id"] == int(brand_id):
      result.append(item)
  return jsonify(result)

# Get Single Coupon
@app.route('/admin/<brand_id>/coupon/<id>', methods=['GET'])
def get_coupon(brand_id, id):
  coupon = Coupon.query.get(id)
  return coupon_schema.jsonify(coupon)

# Update a Coupon's coupon_status
@app.route('/admin/<brand_id>/coupon/<id>/<coupon_status>', methods=['PUT'])
def update_coupon(brand_id, id, coupon_status):
  coupon = Coupon.query.get(id)
  coupon.coupon_status = coupon_status
  db.session.commit()

  return coupon_schema.jsonify(coupon)

# Delete a Coupon
@app.route('/admin/<brand_id>/coupon/<id>', methods=['DELETE'])
def delete_coupon(brand_id, id):
  coupon = Coupon.query.get(id)
  db.session.delete(coupon)
  db.session.commit()

  return coupon_schema.jsonify(coupon)

# USER Endpoints
# Get a discount Coupon for customer
@app.route('/user/<customer_id>/discount_code', methods=['GET'])
def get_coupon_customer(customer_id):
  all_coupons = Coupon.query.all()
  result = coupons_schema.dump(all_coupons)
  list_test= []
  result_data = {}
  for item in result:
    if item['coupon_status'] == 'New':
      coupon_id = int(item['id'])
      coupon = Coupon.query.get(coupon_id)
      coupon_status = "Assigned"
      coupon_user_id = int(customer_id)
      coupon.coupon_status = coupon_status
      coupon.coupon_user_id = coupon_user_id
      db.session.commit()
      result_data ["coupon_string"] = coupon.coupon_string
      result_data["details"] = "Your 10 digits discount code."
      result_data["discount"] = coupon.discount
      break
  return jsonify(result_data)

# Run Servers
if __name__ == '__main__':
  app.run(debug=True)
