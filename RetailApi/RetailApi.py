import argparse
import sys
import json

from flask import Flask, Blueprint
from flask_cors import CORS

from pyspark.sql.session import SparkSession
from pyspark.sql.functions import col
from pyspark.sql import functions as F

try:
    from flask_restplus import Api, Resource, fields
except ImportError:
    import werkzeug, flask.scaffold
    werkzeug.cached_property = werkzeug.utils.cached_property
    flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
    from flask_restplus import Api, Resource, fields

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(api_v1, version='1.0', title='RetailApi', description='RetailApi')


invoice_ns = api.namespace('invoice')
product_ns = api.namespace('product')
customer_ns = api.namespace('customer')

full_product_model = api.model('Product', {
    'stockCode': fields.String(required=True),
    'description': fields.String(required=True),
    'quantity': fields.Integer(required=True),
    'price': fields.Float(required=True)
})

customer_model = api.model('Customer', {
    'id': fields.Integer(required=True)
})

invoice_model = api.model('Invoice', {
    'id': fields.Integer(required=True),
    'date': fields.DateTime(required=True),
    'customer': fields.Nested(customer_model, required=True),
    'country': fields.String(required=True),
    'products': fields.List(fields.Nested(full_product_model), required=True)
})

invoice_product_price_ratio_model = api.model('InvoicePriceQuantityRatio', {
    'country': fields.String(required=True),
    'invoiceDate': fields.DateTime(required=True),
    'invoiceId': fields.Integer(required=True),
    'customerId': fields.Integer(required=True),
    'productPriceRatio': fields.Float(required=True)
})

top_product_model = api.model('TopProduct', {
    'stockCode': fields.String(required=True),
    'description': fields.String(required=True)
})

product_price_distribution = api.model('ProductPriceDistribution', {
    'stockCode': fields.String(required=True),
    'description': fields.String(required=True),
    'averagePrice': fields.Float(required=True)
})

product_country_distribution_model = api.model('ProductCountryDistribution', {
    'stockCode': fields.String(required=True),
    'description': fields.String(required=True),
    'country': fields.String(required=True),
    'count': fields.Integer(required=True)
})


@invoice_ns.route('')
class AllInvoice(Resource):
    @api.marshal_with(invoice_model)
    def get(self):
        '''Group all transactions by invoice'''

        df = init_spark_session()
        df_result = df.select("invoice_id", "invoice_date", "customer_id", "country", "stock_code", "description", "price", "quantity")

        invoice_dic = {}
        for row in df_result.collect():
            current_invoice = {
                "products": []
            }
            if row["invoice_id"] in invoice_dic:
                current_invoice = invoice_dic[row["invoice_id"]]
            else:
                current_invoice["id"] = row["invoice_id"]
                current_invoice["date"] = row["invoice_date"]
                current_invoice["customer"] = {
                    "id": row["customer_id"]
                }
                current_invoice["country"] = row["country"]

                invoice_dic[row["invoice_id"]] = current_invoice
            
            current_invoice["products"].append({
                "stockCode" : row["stock_code"],
                "description" : row["description"],
                "quantity" : row["quantity"],
                "price" : row["price"]
            })
        
        return list(invoice_dic.values())


@invoice_ns.route('/price/quantity/ratio')
class AllPriceQuantityRatioInvoice(Resource):
    @api.marshal_with(invoice_product_price_ratio_model)
    def get(self):
        '''What is the ratio between price and quantity for each invoice?'''

        df = init_spark_session()
        df_result = df.select("country", "invoice_date", "invoice_id", "quantity", "customer_id", (col("quantity") * col("price")).alias("total_price")) \
            .groupBy("invoice_id", "country", "invoice_date", "customer_id") \
            .agg(F.sum("quantity"), F.sum("total_price")) \
            .select("country", col("invoice_date").alias("invoiceDate"), col("invoice_id").alias("invoiceId"), col("customer_id").alias("customerId"), F.round((col("sum(total_price)") / col("sum(quantity)")), 2).alias("productPriceRatio")) \
            .orderBy(col("productPriceRatio").desc())

        return get_reponse_from_spark_json_array(df_result.toJSON().collect())



@product_ns.route('/top')
class TopProduct(Resource):
    @api.marshal_with(top_product_model)
    def get(self):
        '''Which product sold the most?'''

        df = init_spark_session()
        df_result = df.groupBy('stock_code', 'description') \
            .sum("quantity").withColumnRenamed("sum(quantity)", "total_quantity") \
            .orderBy(col("total_quantity").desc()).limit(1)

        result = df_result.first()
        return {
            "stockCode" : result[0],
            "description" : result[1]
        }

@product_ns.route('/average')
class ProductPriceDistribution(Resource):
    @api.marshal_with(product_price_distribution)
    def get(self):
        '''Give a chart showing the distribution of prices'''

        df = init_spark_session()
        df_result = df.groupBy("stock_code", "description").avg("price") \
            .select(col("stock_code").alias("stockCode"), "description",  F.round(col("avg(price)"), 2).alias("averagePrice")) \
            .orderBy(col("averagePrice").desc())

        return get_reponse_from_spark_json_array(df_result.toJSON().collect())

@product_ns.route('/country')
class ProductCountryDistribution(Resource):
    @api.marshal_with(product_country_distribution_model)
    def get(self):
        '''Give a chart showing the distribution of each product for each of the available countries'''
        
        df = init_spark_session()
        df_result = df.groupBy("stock_code", "description", "country").count() \
            .select(col("stock_code").alias("stockCode"), "description",  "country", "count") \
            .orderBy("stockCode", "country")

        return get_reponse_from_spark_json_array(df_result.toJSON().collect())

@customer_ns.route('/top')
class TopProduct(Resource):
    @api.marshal_with(customer_model)
    def get(self):
        '''Which customer spent the most money?'''

        df = init_spark_session()
        df_result = df.select(col("customer_id"), (col("quantity") * col("price")).alias("price")) \
            .groupBy("customer_id").sum("price").withColumnRenamed("sum(price)", "sum_customer_price") \
            .orderBy(col("sum_customer_price").desc()).limit(1)

        return {
	        "id" : df_result.first()[0]
        }

def get_reponse_from_spark_json_array(rows):
    result = []
    for row in rows:
        result.append(json.loads(row))
    return result


def init_spark_session():
    spark = SparkSession.builder.appName("test") \
        .config("spark.mongodb.input.uri", "mongodb://{}:{}/test.retail".format(mongo_host, mongo_port)) \
        .config("spark.mongodb.output.uri", "mongodb://{}:{}/test.retail".format(mongo_host, mongo_port)) \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
        .getOrCreate()

    return spark.read.format("mongo").load()

def parse_argv():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-mongo_host', required=False, default="localhost", help="Set mongodb host")
        parser.add_argument('-mongo_port', required=False, default=27017, type=int, help="Set mongodb port")
        return parser.parse_args()
    except Exception as e:
        sys.exit(2)

if __name__ == '__main__':
    args = parse_argv()
    mongo_host = args.mongo_host
    mongo_port = args.mongo_port
    init_spark_session()

    app = Flask(__name__)
    app.register_blueprint(api_v1)
    cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    app.run("0.0.0.0", 5000)
