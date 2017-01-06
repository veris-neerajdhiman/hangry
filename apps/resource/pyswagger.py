from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
from pyswagger.utils import jp_compose

# from apps.resource import pyswagger


# load Swagger resource file into App object
app = App._create_('http://petstore.swagger.io/v2/swagger.json')

myapp = App._create_('/home/teramatrix/projects/house_of_veris/hangry/apps/resource/swagger.json')

auth = Security(myapp)
auth.update_with('basic', 'token fd80a9654e366ac3a5ded608b25c62f023efb635') # api key
# auth.update_with('petstore_auth', '12334546556521123fsfss') # oauth2

client = Client(auth)

def initilize():
    single = myapp.op['members_read'](id=1)

    all_ = myapp.op['members_list']()

    pet = client.request(all_).data

    # print (pet)
    # print(pets)

def me():
    pet = client.request(app.op['getPetById'](petId=1)).data
