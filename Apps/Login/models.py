from django.db import models
from django.contrib.auth.models import User

corp_type = ((1,'Club deportivo'),(2,'Empresa'),(3,'Particular'))

class IUser(models.Model):
    log_user = models.ForeignKey(User,blank=False,null=False,on_delete=models.CASCADE)    
    class Meta:
        abstract=True
    def __str__(self):
        return "Abstract method __str__()"
    def get_type(self):
        return "Abstract method get_type()"

class Client(IUser):
    corp = models.CharField(max_length=40,blank=True,null=True,default='none')
    client_type = models.IntegerField(choices=corp_type,default=1)
    def __str__(self):
        return "Cliente N°: %s Nombre: %s USUARIO N° %s " %(self.pk,self.log_user.first_name,self.log_user.pk )
    def get_type(self):
        return 'Client'

class Admin(IUser):
    admin_level = models.IntegerField(blank=False,null=False,default=3)
    def __str__(self):
        return "Admin N°: %s Nombre: %s" %(self.pk,self.log_user.first_name)
    def get_type(self):
        return 'Admin'

class User_Factory():
    @staticmethod
    def get_user(user_pk):
        _user_ = User.objects.get(pk=user_pk)
        return _user_
    @staticmethod
    def get_client(client_pk):
        client = Client.objects.get(log_user__pk=client_pk)
        return client
    @staticmethod
    def get_all_cient():
        clients = list(Client.objects.all())
        return clients
    @staticmethod
    def get_type_user(request_user):
        admin = Admin.objects.filter(log_user=request_user).exists()
        client = Client.objects.filter( log_user=request_user).exists()
        if admin:
            return 'admin'
        elif client:
            return 'client'
    @staticmethod
    def register_client(data):
        try:
            new_user = User(username=data['username'], first_name=data['first_name'],last_name=data['last_name'], email=data['email'])
            new_user.set_password(data['password'])
            new_user.save()
            new_client = Client(log_user=new_user, corp=data['corp'], client_type=data['type_corp'])
            new_client.save()
            return True
        except Exception as e :
            if e.__str__() == 'UNIQUE constraint failed: auth_user.username':
                print("Nombre de usuario no disponible")
            elif e.__str__() == 'got an unexpected keyword argument':
                print("Estoy guardando mal un")
            return False

    @staticmethod
    def register_admin(**kwargs):
        pass
    @staticmethod
    def set_data_client(client_pk,data):
        try:
            client = Client.objects.get(log_user__pk=client_pk)
            if data['first_name']:
                client.log_user.first_name = data['first_name']
            if data['last_name']:
                client.log_user.last_name = data['last_name']
                
            if data['email']:
                client.log_user.email = data['email']
            client.log_user.save()
            return True
        except:
            return False
        
    @staticmethod
    def delete_client(client_pk):
        try:
            client = User.objects.get(pk=client_pk)
            #client = Client.objects.get(log_user__pk=client_pk)
            client.delete()
            return True
        except:
            return False


