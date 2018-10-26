from flask import Flask, flash, render_template, send_from_directory, request
from werkzeug.utils import secure_filename
from flask.ext.mysql import MySQL
import os
import file_names
import dns_formatted_name

import threading
import time
from certs import create_certificate_for_client
import uuid
import requests

ACCESS_DENIED = "Access denied"
INDEX_FILE = "index.html"
VALIDATION_FAILURE = "Validation failed please retry again"
MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_PASSWORD = 'cns'
MYSQL_DATABASE_DB = 'ncs'
MYSQL_DATABASE_HOST = 'localhost'
TABLE_NAME = 'ncs.name_data'
MYSQL_DATABASE_PORT = 3306
USER_ID_FIELD_NAME = 'user_id'
IDENTIFIER_FIELD_NAME = 'identifier'
NAME_CONFLICT_ERROR= 'Name Conflict, please try with another name'
KEY_PREFIX = 'cert_'
KEY_SUFFIX = '.crt'
PROOF_PREFIX = 'proof_'
PROOF_SUFFIX = '.proof'

CERTIFICATE_STORE = '/certificates/'
PRIVATE_KEY_STORE = '/private_keys/'



# TODO find out when to intialize these stuff
app = Flask(__name__, template_folder='template')
mysql =  MySQL()
cursor = ""


# placeholder function to do server side validation
# returns 1 on success
def validate_fields(data_request):
    return 1


# helper function to check if any entry exists with same name
def check_name_conflict(domain_name):
    
    query_statement = "SELECT " + USER_ID_FIELD_NAME + " FROM " + TABLE_NAME + " WHERE " +  IDENTIFIER_FIELD_NAME + "='%s'" % (domain_name)

    conn = mysql.connect()
    cursor = conn.cursor()

    result = cursor.execute(query_statement)
    data = cursor.fetchone()
    if data == None:
        return False

    else:
        return True


def get_dns_formatted_name(arbitary_string):
    return arbitary_string

# Insert fields into database
# returns 1 on success
def insert_fields_into_database(data_request):
    # read all variables into local

    

    first_name = data_request.form['first_name']
    last_name = data_request.form['last_name']

    email = data_request.form['email']
    phone = data_request.form['phone']

    address = data_request.form['address'] + " "
    address += data_request.form['city'] + " "
    address += data_request.form['state'] + " "
    address += data_request.form['country']

    identifier = data_request.form['website']
    gns_provider = data_request.form['gns_provider']

    certificate_file_name = file_names.get_certificate_name(identifier)

    
    query_statement = " INSERT into " + TABLE_NAME + " " + \
                        " (first_name,last_name, email, mobile, address, identifier, gns_provider, certificate_file_name, verified) " + \
                        " VALUES ('" + first_name + "' , '"+ last_name +"', '"+ email + "', '" + phone + "', '" + address +"', '"+ identifier + "', '"+ gns_provider +"','"+ certificate_file_name +"' ,0)"   

    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute(query_statement)
    conn.commit()

    return 1

#validate path obtained while serving static pages 
def validate_uri(path):
    return 1

# send static javascript files  
@app.route('/js/<path:path>')
def send_js(path):
    if (validate_uri(path)  == 1 ) :
        return send_from_directory('js', path)
    else :
        return ACCESS_DENIED

# send static css files 
@app.route('/css/<path:path>')
def send_css(path):
    if (validate_uri(path)  == 1 ) :
        return send_from_directory('css', path)
    else :
        return ACCESS_DENIED

# send static certificate files
@app.route('/certificates/<path:path>')
def send_certificate(path):
    if (validate_uri(path)  == 1 ) :
        return send_from_directory('certificates', path)
    else :
        return ACCESS_DENIED

# send static private keys
@app.route('/private_keys/<path:path>')
def send_private_key(path):
    if (validate_uri(path)  == 1 ) :
        return send_from_directory('private_keys', path)
    else :
        return ACCESS_DENIED


# send index file on request 
@app.route('/')
def hello():
    return send_from_directory('template', 'index.html')


# utility function read values from request
def get_details_from_request(data_request):

    client_details= {}
    client_details['name'] = data_request.form['first_name'] + data_request.form['last_name']
    client_details['state'] = data_request.form['state']
    client_details['mail'] = data_request.form['email']
    client_details['city'] = data_request.form['city']
    client_details['domain_name'] = data_request.form['website']
    client_details['country'] =  data_request.form['country']

    return client_details


def make_default_entry(cert_path,private_path):

    local_cert_path = "./" + cert_path
    local_private_path = "./" + private_path
    
    url = 'http://gns.opengns.com/makedefaultentry'
    files = {'file1': open(local_cert_path), 'file2':open(local_private_path)}
    try:
        response = requests.post(url, files=files)
    except:
        print "Unexpected error occurred while making the default entry"



# create certificate and mail to the client
def send_certificate_to_client(client_details):
    #create public-private key pair for user
    sub_domain_name = dns_formatted_name.get_dns_formatted_subdomain(client_details['domain_name'])
    shell_cmd = "./create_public_private_pair.sh " + sub_domain_name
    os.system(shell_cmd)

    create_certificate_for_client(client_details)

    certificate_file_name = file_names.get_certificate_name(client_details['domain_name'])
    total_cert_path = CERTIFICATE_STORE + certificate_file_name

    private_key_file_name = file_names.get_private_key_name(client_details['domain_name'])
    total_private_key_path = PRIVATE_KEY_STORE +  private_key_file_name

    
    make_default_entry(total_cert_path, total_private_key_path)
    return render_template("success.html", certificate_path=total_cert_path, private_key_path=total_private_key_path)



# receive and process the data 
@app.route('/submitdata',  methods=['POST'])
def process_request():

    if request.method == 'POST':

    
        # do server validation of fields 
        if ( validate_fields(request) == 1) :

            #check for name conflict
            if check_name_conflict(request.form['website']) == True:
                 return NAME_CONFLICT_ERROR

            insert_result = insert_fields_into_database(request)

            if (insert_result == 1):
                return send_certificate_to_client(get_details_from_request(request))

            else:
                return "Unknown error has occured while inserting into database \n"

        else :
            return VALIDATION_FAILURE


# init mysql config
def init_mysql_config():
    app.config['MYSQL_DATABASE_USER'] = MYSQL_DATABASE_USER
    app.config['MYSQL_DATABASE_PASSWORD'] = MYSQL_DATABASE_PASSWORD
    app.config['MYSQL_DATABASE_DB'] = MYSQL_DATABASE_DB
    app.config['MYSQL_DATABASE_HOST'] = MYSQL_DATABASE_HOST
    app.config['MYSQL_DATABASE_PORT'] = MYSQL_DATABASE_PORT
    mysql.init_app(app)
    

# main method 
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = "./"
    app.config['UPLOAD_PROOF'] = "./proof/"
    app.config['UPLOAD_KEY'] = "./public_keys/"
    init_mysql_config()
    app.run(host='0.0.0.0', port=80)

