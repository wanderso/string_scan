from flask import Flask
import test_data_producer
import os.path

APP = Flask(__name__.split('.')[0])

@APP.route("/")
def home_page():
    with open("html/main_search.html") as fh:
        return fh.read()

@APP.route("/<file_name>")
def static_page(file_name):
    basename = file_name.rsplit('..', 1)[0]
#    safe_file_name = os.path.join("html/", basename)
    test_dat = test_data_producer.calculate_string_probability_for_target([basename])
    return ("The artificial intelligence believes that %s is a part of type %s" % (test_dat[0][0],test_dat[0][1]))

if __name__ == "__main__":
    # Run on port 8003, allow connections from all IP addresses
    APP.run(port=8003, host='127.0.0.1', debug=True)