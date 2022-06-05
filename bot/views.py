import os
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from twilio.rest import Client

from bot.forms import bot_tracking_form
from bot.models import bo_bot_message, bo_bot_tracking
from users.forms import PersonForm
from users.models import Person

from files.models import Fi_file, Fi_file_type

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

@csrf_exempt
def bot(request):
    #print(request.POST)
    messagesBody = request.POST.get('Body')
    profileName = request.POST.get('ProfileName')
    phoneReceiver = request.POST.get('From')
    phoneSandbox = request.POST.get('To')
    AccountSidd = request.POST.get('AccountSid') if request.POST.get('AccountSid') != None else ''
    responseMessage = ''

    phoneReceiverCleaned = cleanValues(phoneReceiver)
    #phoneSandboxCleaned = cleanValues(phoneSandbox)
    #Numeros limpios sin whatsapp:

    try:
        qsTracking = bo_bot_tracking.objects.get(phoneMessageFrom=phoneReceiverCleaned)
    except bo_bot_tracking.DoesNotExist:
        qsTracking = None
    #valido si existe un historial de telefono en el tracking
    if qsTracking:
        #valida si el tracking path tiene submenu
        match qsTracking.trackingPath:
            case '0':

                goHomeMenu(profileName,phoneSandbox,phoneReceiver,phoneReceiverCleaned,messagesBody,AccountSidd)
                response = HttpResponse("response data")
                response.delete_cookie('sessionfiletypeid')
                return response
            case '1':

                match messagesBody:
                    case '1': #Mis documentos

                        try:
                            #idUser = request.COOKIES['sessionUserid']
                            idUser = qsTracking.user.id
                            if idUser:
                                userObj = User.objects.get(pk=idUser)
                            else:
                                userObj = None
                        except Person.DoesNotExist as ex:
                            userObj = None
                            responseMessage = 'El usuario no existe, crea una cuenta desde la pagina web'
                            createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                            return HttpResponse('send error no existe')
                        if userObj:
                            responseMessage = ''
                            objFileType = Fi_file_type.objects.filter(isActive=1, user=userObj).order_by('id')
                            if objFileType:
                                responseMessage = 'Seleciona el archivo a descargar 😄\n'
                                for i,item in enumerate(objFileType, start=1):
                                    responseMessage += f"*{i}.* {item.name} \n"
                                createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                                create_or_update_tracker(phoneReceiverCleaned,'1.1',messagesBody,AccountSidd,True)
                                return HttpResponse('success')
                            else:
                                responseMessage = 'No tienes documentos creados aún 🤔 \n Crealos en la pagina web'
                                createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                                create_or_update_tracker(phoneReceiverCleaned,'0',messagesBody,AccountSidd,True)
                                return HttpResponse('send session error')
                        else:
                            responseMessage = 'Inténtalo de nuevo más tarde, algo salió mal'
                            createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                            return HttpResponse('send session error')
                    case '2': #Mis Carpetas
                        pass
                    case '3': #Sitio web
                        try:
                            obj = bo_bot_message.objects.get(resume='3')
                            responseMessage = obj.message.format(request.build_absolute_uri('/')[:-1],'Volver atrás')
                        except bo_bot_message.DoesNotExist as e:
                            obj = None
                            responseMessage = 'Inténtalo de nuevo más tarde'
                        createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                        create_or_update_tracker(phoneReceiverCleaned,'0',messagesBody,AccountSidd,True)
                    case _:
                        try:
                            obj = bo_bot_message.objects.get(resume='1')
                            responseMessage = obj.message.format(profileName,'Mis documentos','Mis Carpetas','Sitio web')
                        except bo_bot_message.DoesNotExist as e:
                            obj = None
                            responseMessage = 'Inténtalo de nuevo más tarde'
                        createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                        create_or_update_tracker(phoneReceiverCleaned,'1',messagesBody,AccountSidd,True)

            case '1.1':

                if messagesBody.isdigit() and int(messagesBody) > 0:
                    try:
                        idUser = qsTracking.user.id
                        if idUser:
                            userObj = User.objects.get(pk=idUser)
                        else:
                            userObj = None
                    except Person.DoesNotExist as ex:
                        userObj = None
                        responseMessage = 'El usuario no existe, crea una cuenta desde la pagina web'
                        createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                        return HttpResponse('send error no existe')
                    if userObj:
                        objFileType = Fi_file_type.objects.filter(isActive=1, user=userObj).order_by('id')
                        try:
                            objFileTypeSelected = objFileType[int(messagesBody)-1]
                        except IndexError:
                            objFileTypeSelected = None
                        if objFileTypeSelected:
                            try:
                                
                                objFile = Fi_file.objects.filter(fileType_id=objFileTypeSelected.id).order_by('id')
                                if objFile.exists():
                                    responseMessage = 'Escriba el numero relacionado para continuar 😄\n'
                                    for i,item in enumerate(objFile, start=1):
                                        responseMessage += f"*{i}.* {item.fileTypeName} \n"
                                    createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                                    create_or_update_tracker(phoneReceiverCleaned,'1.1.1',messagesBody,AccountSidd,True)
                                    response = HttpResponse("Cookie Set")
                                    response.set_cookie('sessionfiletypeid', objFileTypeSelected.id)
                                    return response
                                else:
                                    #nohaymessage
                                    responseMessage = 'No hay archivos en esta carpeta 🤔\n Selecciona la opción existente o regresa al menú *0*'
                                    createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                                    return HttpResponse('send error no existe')
                            except:
                                objFileTypeSelected = None
                                print(f'No hay objeto en la posición {int(messagesBody)-1}')
                        else:
                            print('No hay objeto')
                            responseMessage = 'No existe la carpeta seleccionada 🤔\n Selecciona la opción existente o regresa al menú *0*'
                            createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                            return HttpResponse('send error no existe')

                    else:
                        responseMessage = 'Inténtalo de nuevo más tarde, algo salió mal'
                        createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                        return HttpResponse('send session error')
                
                elif messagesBody == '0':
                    #nohaymessage
                    goHomeMenu(profileName,phoneSandbox,phoneReceiver,phoneReceiverCleaned,messagesBody,AccountSidd)
                    response = HttpResponse("response data")
                    response.delete_cookie('sessionfiletypeid')
                    return response
                
                else:
                    #nohaymessage
                    responseMessage = 'Opción incorrecta 🤔\n Ingresa un numero valido'
                    createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                    create_or_update_tracker(phoneReceiverCleaned,'1.1',messagesBody,AccountSidd,True)
                    return HttpResponse('send error incorrecto')
                    
            case '1.1.1':

                if messagesBody.isdigit() and int(messagesBody) > 0:
                    try:
                        idUser = qsTracking.user.id
                        if idUser:
                            userObj = User.objects.get(pk=idUser)
                        else:
                            userObj = None
                    except Person.DoesNotExist as ex:
                        userObj = None
                        responseMessage = 'El usuario no existe, crea una cuenta desde la pagina web'
                        createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                        return HttpResponse('send error no existe')

                    try:
                        objFileTypeId = request.COOKIES['sessionfiletypeid']
                        objFile = Fi_file.objects.filter(fileType_id=objFileTypeId).order_by('id')
                        if objFile.exists():
                            try:
                                objFileSelected = objFile[int(messagesBody)-1]
                            except IndexError:
                                objFileSelected = None
                            
                            if objFileSelected:
                                fileUrl = ''
                                if str(os.getenv('USE_S3_CLOUD')) == "1":
                                    fileUrl = objFileSelected.files.url
                                else:
                                    print(objFileSelected.files.url+'-'+objFileSelected.files.name)
                                    fileUrl = request.build_absolute_uri('/')[:-1] + objFileSelected.files.url
                                responseMessage = f'Se ha generado el documento 📄\n ⬅ Volver al menú principal'
                                createMessage(responseMessage,phoneSandbox,phoneReceiver,True,fileUrl)
                                create_or_update_tracker(phoneReceiverCleaned,'0',messagesBody,AccountSidd,True)
                                return HttpResponse('success')
                            else:
                                #Object doesn't exist (Index out)
                                print('No hay objeto')
                                responseMessage = 'No existe la carpeta seleccionada 🤔\n Selecciona la opción existente o regresa al menú *0*'
                                createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                                return HttpResponse('send error no existe')
                        else:
                            #nohaymessage
                            responseMessage = 'No hay archivos en esta carpeta 🤔\n Selecciona otra carpeta o regresa al menú enviando *0*'
                            createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                            return HttpResponse('send error no existe')
                    except:
                        objFileTypeSelected = None
                        print(f'No hay objeto en la posición 1.1.1 {int(messagesBody)-1}')
                
                elif messagesBody == '0':
                    #nohaymessage
                    goHomeMenu(profileName,phoneSandbox,phoneReceiver,phoneReceiverCleaned,messagesBody,AccountSidd)
                    response = HttpResponse("response data")
                    response.delete_cookie('sessionfiletypeid')
                    return response
                else:
                    #nohaymessage
                    responseMessage = 'Opción incorrecta 🤔\n Ingresa un numero valido'
                    createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
                    create_or_update_tracker(phoneReceiverCleaned,'1.1',messagesBody,AccountSidd,True)
                    return HttpResponse('send error incorrecto')

                    


            case '1.2':
                print('fumadon caleño1.2')
            case '1.3':
                print('fumadon caleño1.3')
            case '2':
                print('fumadon caleño2')
            case '2.1':
                print('fumadon caleño2.1')
            case '2.2':
                print('fumadon caleño2.2')
            case '2.3':
                print('fumadon caleño2.3')
            case _:
                print('fumadon Any')

    else:
        try:
            personObj = Person.objects.get(phone_number=phoneReceiverCleaned)
        except Person.DoesNotExist as ex:
            personObj = None
            createMessage("No tienes registrado numero de teléfono, crea uno ingresando a la pagina web",phoneSandbox,phoneReceiver,False)
            return HttpResponse('Send error')
        if personObj:
            try:
                userObj = User.objects.get(pk=personObj.user.id)
            except Person.DoesNotExist as ex:
                userObj = None
                createMessage("El usuario no existe, crea una cuenta desde la pagina web",phoneSandbox,phoneReceiver,False)
                return HttpResponse('send error no existe')

            if userObj:
                objTracking = create_or_update_tracker(phoneReceiverCleaned,'0',messagesBody,AccountSidd,False,userObj)

                if objTracking:
                    objTracking.save()
                else:
                    createMessage("No tienes registrado numero de teléfono, crea uno ingresando a la pagina web",phoneSandbox,phoneReceiver,False)
                    return HttpResponse('send error formulario no valido')
                
                createMessage("Bienvenido",phoneSandbox,phoneReceiver,False)
                response = HttpResponse("Cookie Set")
                response.set_cookie('sessionUserid', userObj.id)
                return response
                # request.session['sessionTracking'] = objTracking.trackingPath

    return HttpResponse("Holaa")

def create_or_update_tracker(phone,trakingPath, lstMsj, authSid,isUpdate,userObj=None):

    if isUpdate:
        objTracking = bo_bot_tracking.objects.get(phoneMessageFrom=phone)
        objTracking.trackingPath=trakingPath
        objTracking.lastMessage=lstMsj
        objTracking.AccountSid= authSid
        data = objTracking.save()
        return data
    else:
        try:
            objTracking = bo_bot_tracking(user=userObj,trackingPath=trakingPath,lastMessage=lstMsj,phoneMessageFrom=phone, AccountSid=authSid)
        except:
            objTracking = None
        return objTracking

def createMessage(msj,phoneApi,phone,mediaBool,media=None):
    if mediaBool:
        client.messages.create(
            media_url=media,
            body=msj,
            from_=phoneApi,
            to=phone)
    else:
        client.messages.create(
            body=msj,
            from_=phoneApi,
            to=phone)

def cleanValues(text):
    charFind = text.find(':')
    if charFind == -1:
        return text
    return text[text.find(':')+1:]



def listBot(request):
    obj = bo_bot_message.objects.all()
    context = {
        'objBot': obj
    }

    return render(request, 'bot/list.html', context)


def goHomeMenu(profileName,phoneSandbox,phoneReceiver,phoneReceiverCleaned,messagesBody,AccountSidd):
    try:
        obj = bo_bot_message.objects.get(resume='1')
        responseMessage = obj.message.format(profileName,'Mis documentos','Mis Carpetas','Sitio web')
        createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
        create_or_update_tracker(phoneReceiverCleaned,'1',messagesBody,AccountSidd,True)
    except bo_bot_message.DoesNotExist:
        responseMessage = 'Inténtalo de nuevo más tarde'
        createMessage(responseMessage,phoneSandbox,phoneReceiver,False)
