from django.shortcuts import render, redirect, HttpResponse
import pyrebase
from django.contrib import auth
from model.models import data
from django.template import RequestContext, response
from django.shortcuts import render_to_response
from django.http import JsonResponse
import json
import datetime

config = {

    'apiKey': "AIzaSyDZxw1qSdXuHDLseNh2y3TN-O8NfhpPoQc",
    'authDomain': "cpanel-c54b7.firebaseapp.com",
    'databaseURL': "https://cpanel-c54b7.firebaseio.com",
    'projectId': "cpanel-c54b7",
    'storageBucket': "cpanel-c54b7.appspot.com",
    'messagingSenderId': "82198444165",
    'appId': "1:82198444165:web:eb9e20a95d9fcaacd991ec",
    'measurementId': "G-E595RHEXVP"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()


def signIn(request):
    try:
        uid = request.COOKIES['uid']
    except:
        return render(request, "index_login.html")
    return redirect('/listdevices/')


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    remembr_me = request.POST.get("remember-me")
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "index_login.html", {"messg": message})
    print(user['idToken'])
    print(user['localId'])
    # response = render_to_response( 'welcome.html', {"e": email})
    response = redirect("/")
    uid = user['localId']
    if not remembr_me:
        response.set_cookie('uid', uid)
    else:
        response.set_cookie('uid', uid, 2592000)
    return response


def logout(request):
    return render(request, 'signIn.html')


def signUp(request):
    return render(request, "signup.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", {"messg": message})

    data = {"name": name}

    database.child("users").child(uid).child("details").set(data)
    return render(request, "signIn.html")


#############################################################################################################################################################################


def list_devices(request):
    uid = request.COOKIES['uid']
    devices_dict = database.child('users').child(uid).shallow().get().val()
    devices_list = []
    for device in devices_dict:
        devices_list.append(device)

    print(devices_list)
    return render(request, "list_devices.html", {'devices': devices_list})


def device_data(request):
    uid = request.COOKIES['uid']
    deviceID = request.GET.get('z')
    data_timing = database.child('Data').child(deviceID).get().val()
    keys = []
    for key in data_timing.keys():
        keys.append(str(key))
    print(keys)
    keys = reversed(keys)
    data_timing = json.dumps(data_timing)
    # print(time)
    response = json.loads(data_timing)
    current = []
    temperature = []
    voltage = []
    for key in keys:
        curr = response[key]['Current']
        temp = response[key]['Temperature']
        pd = response[key]['Voltage']
        # print("Current:" + str(curr) + "      Temperature:" + str(temp) + "      Voltage:" + str(pd))
        current.append(curr)
        temperature.append(temp)
        voltage.append(pd)
    comb_lis = zip(current, temperature, voltage)
    return render(request, "device_data.html", {'comb': comb_lis})


def ajax_update(request):
    # uid = request.COOKIES['uid']
    deviceID = request.GET.get('z')
    data_timing = database.child('Data').child(deviceID).get().val()
    # print(data_timing)
    keys = []
    for key in data_timing.keys():
        keys.append(str(key))
    # print(keys)
    keys = reversed(keys)
    data_timing = json.dumps(data_timing)
    # print(time)
    response = json.loads(data_timing)
    time = []
    current = []
    temperature = []
    voltage = []
    humidity = []
    for key in keys:
        tim = response[key]['Time']
        curr = response[key]['Current']
        temp = response[key]['Temperature']
        pd = response[key]['Voltage']
        humi = response[key]['Humidity']
        # print("Current:" + str(curr) + "      Temperature:" + str(temp) + "      Voltage:" + str(pd))
        time.append(tim)
        current.append(curr)
        temperature.append(temp)
        voltage.append(pd)
        humidity.append(humi)

    comb_lis = zip(time, current, temperature, voltage, humidity)
    return JsonResponse({"comb_lis": list(comb_lis)})


def ajax_index(request):
    return render(request, "ajax_index.html")


def save_latest_data(request):
    users_dict = database.child('users').shallow().get().val()
    # Getting Users List
    user_list = []
    for user in users_dict:
        user_list.append(user)

    # Nested List For Saving Values
    for user in user_list:
        devices_dict = database.child('users').child(user).shallow().get().val()
        devices_list = []
        for device in devices_dict:
            devices_list.append(device)
        # print(devices_list)
        for device in devices_list:
            # print(device)
            data_packets = database.child('Data').child(device).get().val()
            # print(data_packets)
            keys = []
            try:
                for key in data_packets.keys():
                    keys.append(str(key))
                    # print(keys)
                    data_packets = json.dumps(data_packets)
                    response = json.loads(data_packets)
                    for key in keys:
                        tim = response[key]['Time']
                        curr = response[key]['Current']
                        temp = response[key]['Temperature']
                        pd = response[key]['Voltage']
                        humi = response[key]['Humidity']
                        print(str(user) + "/" + str(device) + "/" + str(key) + "")
                        print("Time:" + str(tim) + "      Current:" + str(curr) + "      Temperature:" + str(
                            temp) + "      Voltage:" + str(pd) + "      Humidity:" + str(humi))
                        tim = datetime.datetime.strptime(tim, '%Y-%m-%d %H:%M:%S')
                        save_data(user=user, device_no=device, time=tim, current=curr, temperature=temp, voltage=pd,
                                  humidity=humi)
                        database.child('Data').child(device).child(key).remove()
            except:
                return HttpResponse("<h1>No data pending...</h1>")
    return HttpResponse("<h1>Done....</h1>")


def save_data(user, device_no, time, current, temperature, voltage, humidity):
    dataToSave = data.objects.create(
        user=user,
        device_no=device_no,
        time=time,
        current=current,
        temperature=temperature,
        voltage=voltage,
        humidity=humidity,
    )
    dataToSave.save()


def filter_data(request):
    uid = request.COOKIES['uid']
    deviceID = request.GET.get('z')
    min_time = None
    max_time = None
    min_query = "SELECT id,MIN(time) FROM model_data WHERE user = '" + uid + "' AND device_no = '" + str(deviceID) + "'"
    max_query = "SELECT id,time FROM model_data WHERE user = '" + uid + "' AND device_no = '" + str(deviceID) + "'"
    for i in data.objects.raw(min_query):  # This query gives MIN time
        min_time = i.time
    for i in data.objects.raw(max_query):  # This query gives MAX time don't know how
        max_time = i.time
    print(min_time)
    print(max_time)
    min_date = str(min_time)[0:10]
    max_date = str(max_time)[0:10]
    return render(request, "filter_data.html", {'min': min_date, 'max': max_date})
