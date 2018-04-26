toil
---
Hard working python framework with boots on the ground for your cloud.
                              ~~~~~~~~
                               ~~~~~~
                              ~~~~~~~~
        /-\
       |< >|
        \@/
        /|\
         | \
        / \ \
          ___\___
          | | | |

Description
---
The toil Python framework is for cloud administrators or programmers
requiring access to cloud services.

Built in providers for OCI, AWS, CHEF, SCALR, RELATIONAL DATA SOURCES.

Provides a simplistic pattern to develop and utilize services
that will help you get off the ground and into the cloud quickly. The code
follows the "Convention over Configuration" design paradigm. Services are
completely exposed so you do not have to worry about the framework hiding
implementation details.

The framework is extensible by allowing you to add your own services.

Encryption, method decorators for timing and retry, and other utilities are
available.

Get the code at https://github.com/drewncrew/toil.git

Whats New?
----
- 2018-04-26 First release


Usage
----
Here is a quick glance demonstrating how easy it is:

###### Create Framework
```
# process args
args = parm.handle.handle_parms(['c', 'k'])

# create cloud framework
framework = toil.create(**args)
```

###### OCI (Oracle cloud infrastructure)
```
session = framework.oci.session(env)
compute_client = session.client('compute')
instances = session.paginate(compute_client.list_instances, session.config()['compartment_id'])

for instance in instances:
logger.info(instance)
```

###### OpenStack
```
session = framework.openstack.session()
openstack_connection = session.connect()

for server in openstack_connection.compute.servers():
meta = server.metadata.get('some-key')
```

###### Scalr
```
session = framework.scalr.session()
scalr_envs = session.list('/account/environments/')
```

###### AWS
```
instance = framework.aws.resource('ec2', 'default').Instance('i-xxxxxxx')
tags = instance.tags
```

###### AWS S3 upload directory
```
framework.aws.upload_to_s3('some-bucket', '/path to dir', 'folder name')
```

###### AES enryption
```
key = framework.encryptor.generate_key()
confidential_data = "this is an encryption test"
encrypted_data = toil.encryptor.encrypt(confidential_data, encryption_key=key)
decrypted_data = toil.encryptor.decrypt(encrypted_data, encryption_key=key)
```

######A service you provide becomes a property of the library.  Pretty cool!
```
my_service_session = framework.your_service.session()
my_service_session.your_method()
```

###### Method execution metrics
```
@util.decorator.timeit(loops=1)
def process(toil):
...
```

###### Retry if an exception occurs
```
@util.decorator.retry(3, requests.exceptions.RequestException)
def get(self, url, **kwargs):
...
```

###### execute a sql statement
```
# execute a query
---------------
q = """
select
*
from
cur_instance
where
instance_id like :i
"""

# simple query
---------------
ds_session = framework.datasource.session()

for row in ds_session.exec_sql_query(q, **{"i": "i-30%"}):
print(row['instance_id'])
```

It it that easy?
---------------
Yes it really is easy, just install required software and create a config
file.

See Install section.

What's up with the parameters to create library?
---------------
###### Standard parameters include:
-  -c = config file
-  -e = environment
-  -k = encryption key
-  -o = options
-  -v = verbose

What does the config file look like?
---------------
The config file is JSON.

Each service may have multiple profiles defined.  For instance, you may have
an OCI admin profile, OCI basic profile and OCI read only profile.  You may specify
different credentials in each profile.

Each data source and service may have 1-M profiles.  A profile named 'default' is used
in all method calls if no profile name is provided.

###### For instance:
```
framework.oci.session('oci_profile_1')
```


``` json
{
"toil": {
"datasources": {
"default": {
"log_level": "info",
"provider": "provider.datasource.AlchemyMySQLDatasourceProvider",
"proxy": "",
"adapter": "mysql+pymysql",
"database": "db_name",
"env": "db_env",
"host": "host_name",
"port": "3306",
"user": "user",
"password": "password"
}
},
"services": {
"oci": {
"alias": "oci",
"log_level": "debug",
"provider": "provider.oci_sdk.OciSdkLib",
"proxy": "",
"default": {
"user": "ocid1.user.oc1...",
"fingerprint": "...",
"key_file": "~/.oci/oci_api_key.pem",
"tenancy": "ocid1.tenancy.oc1...",
"region": "us-ashburn-1"
},
"oci_profile_1": {
"user": "ocid1.user.oc1...",
"fingerprint": "...",
"key_file": "~/.oci/oci_api_key.pem",
"tenancy": "ocid1.tenancy.oc1...",
"region": "us-ashburn-1"
},
"oci_profile_2": {
"user": "ocid1.user.oc1...",
"fingerprint": "...",
"key_file": "~/.oci/oci_api_key.pem",
"tenancy": "ocid1.tenancy.oc1...",
"region": "us-ashburn-1"
}
},
"aws": {
"alias": "aws",
"log_level": "info",
"provider": "provider.aws.AwsLib",
"proxy": "proxy-host-name:proxy-port",
"default": {
"access_key_id": "access_key_id",
"account_number": "account_number",
"region": "us-east-1",
"role_arn": "arn:aws:iam::#########:role/role-name",
"role_session_name": "role_session_name",
"secret_access_key": "secret_access_key"
},
"aws_profile_1": {
"access_key_id": "access_key_id",
"account_number": "account_number",
"region": "us-east-1",
"role_arn": "arn:aws:iam::#########:role/role-name",
"role_session_name": "role_session_name",
"secret_access_key": "secret_access_key"
}
},
"chef": {
"alias": "chef",
"log_level": "debug",
"provider": "provider.chefapi.ChefLib",
"proxy": "",
"default": {
"chef_server_url": "chef_server_url",
"client_key": "client_key/path/some.pem",
"ssl_verify": false,
"user": "user"
}
},
"openstack": {
"alias": "openstack",
"log_level": "info",
"provider": "provider.openstack.OpenStackLib",
"proxy": "",
"default": {
"auth_url": "auth_url",
"domain": "domain",
"password": "password",
"project": "project",
"region": "region",
"user": "user",
"user_domain": "user_domain"
}

},
"openstack_sdk": {
"alias": "openstack_sdk",
"log_level": "info",
"provider": "provider.openstack_sdk.OpenStackLib",
"proxy": "",
"default": {
"auth_url": "auth_url",
"domain": "domain",
"password": "password",
"project": "project",
"region": "region",
"user": "user"
}
},
"scalr": {
"alias": "scalr",
"log_level": "info",
"provider": "provider.scalr.ScalrLib",
"proxy": "",
"default": {
"api_key_id": "api_key_id",
"api_key_secret": "api_key_secret",
"api_url": "api_url",
"project_id": "project_id"
}
}
}
}
}
```
How do I create a config file?
---------------
- generate encryption keys (optional)
- create a config file - sample code in project
- add credentials and passwords to config
- encrypt the config file. (optional)
- use the config file

```
config_file = 'c:/temp/toil.json'
encrypted_file = 'c:/temp/toil_enc.json'
decrypted_file = 'c:/temp/toil_denc.json'

# generate a config file
config.util.generate_config_file(config_file)

#now update the file with credentials and passwords.

# encrypt file (optional)
key = toil.encryptor.generate_key('/Users/andrewlove/projects-github/config/toil_key.txt')
framework.encrypt_config_file(config_file, encrypted_file, encryption_key=key)

# decrypt file (optional)
framework.decrypt_config_file(encrypted_file, decrypted_file, encryption_key=key)
```

How do I add my own service?
---------------

###### create a class inherits from provider.base.BaseProvider
###### implement the session method
```
# -*- coding: utf-8 -*-
"""
Example custom service
"""
import logging
import util.decorator
import provider.base
import toil

logger = logging.getLogger(__name__)


class ExampleLib(provider.base.BaseProvider):
"""
Class example

Properties :
config: dict with configuration data
"""

def __init__(self, cloud_provider, config):
super(ExampleLib, self).__init__(cloud_provider, config)

def session(self, profile='default'):
"""
Create session.

Args:
profile (str): the profile defined in config to use

Returns:
Session
"""
if profile in self.config:
self.configure_proxy()
session = ExampleSession(self,
api_url=self.config[profile]['api_url'],
api_key_id=self.config[profile]['api_key_id'],
api_key_secret=self.config[profile]['api_key_secret']
)
return session
else:
raise toil.CloudException(
"profile '{profile}' not defined in config {config}".format(profile=profile, config=self.config))


class ExampleSession(object):
"""
example
"""
def __init__(self, client, api_url, api_key_id, api_key_secret):
self.client = client
self.api_url = api_url
self.api_key_id = api_key_id
self.api_key_secret = api_key_secret
super(ExampleSession, self).__init__()

def list(self, path, **kwargs):
return []

def create(self, *args, **kwargs):
return {}

def fetch(self, *args, **kwargs):
return {}

def delete(self, *args, **kwargs):
return {}

def post(self, *args, **kwargs):
return {}

@util.decorator.retry(3, Exception)
def get(self, url, **kwargs):
return {}
```

###### add service to config file.  Alias is used as the property name on the library.
``` json
"services": {
"example_service": {
"provider": "provider.example.ExampleLib",
"alias": "example_service",
"log_level": "info",
"proxy": "",
"default": {
"account_number": "123",
"access_key_id": "456",
"secret_access_key": "789",
}
"profile2": {
"account_number": "abc",
"access_key_id": "def",
"secret_access_key": "ghi",
}
}

...
```

###### use your service
```
session = toil.example_service.session( )
session.fetch( )
```

Examples
----
Review the exmple package.
Get the code at https://github.com/drewncrew/toil.git


Installation
---------------
####Linux

######create a projects directory
```
mkdir ~/projects
cd ~/projects
```


######ensure python 2.7.6. is installed (Only do this if installing python)
```
sudo yum groupinstall -y 'development tools'
sudo yum install -y python-devel
sudo yum install -y xz-libs
sudo yum install -y zlib-devel
sudo yum install -y openssl-devel
sudo yum install -y openldap-devel
sudo yum install -y mysql-devel.x86_64
sudo yum install -y mysql-connector-python
```

###### get python source (Only do this if installing python)
```
wget http://www.python.org/ftp/python/2.7.12/Python-2.7.12.tar.xz
# decode (-d) the XZ encoded tar archive:
xz -d Python-2.7.12.tar.xz
# extraction:
tar -xvf Python-2.7.12.tar
```

###### build python 2.7 (Only do this if installing python)
```
cd Python-2.7.12
./configure
sudo make
sudo make altinstall
#python2.7 should now be in /usr/local/bin/
```

######ensure pip is installed
```
wget https://bootstrap.pypa.io/get-pip.py
sudo /usr/local/bin/python2.7 get-pip.py
#pip2.7 should now be in /usr/local/bin/
```


###### install virtual environment
```
cd ~/projects
sudo /usr/local/bin/pip2.7 install virtualenv
```

###### activate virtual environment
```
virtualenv --python=/usr/local/bin/python2.7 toilpython27
source ~/projects/bin/activate
```

######finally install the library
```
#get the current source distribution
wget -O /dist/toil-0.0.1.tar.gz
pip2.7 install -I /home/user/projects/myproject/toil-0.0.1.tar.gz
```

######create a directory for your project
```
mkdir ~/projects/myproject
cd ~/projects/myproject/
#makesure your virtual env is active
source ~/projects/bin/activate
which python #should return ~/projects/toilpython27/bin/python
```

######notes
- get the 2.7 release from https://www.python.org/downloads/
- install .whl by ```pip install some-package.whl```
- http://dev.mysql.com/downloads/connector/python/
- get the current source distribution at https://github.com/drewncrew/toil.git/raw/master/dist/
- pip install -I toil-0.0.1.tar.gz
- Create a source distribution with command python setup.py sdist --formats=gztar
