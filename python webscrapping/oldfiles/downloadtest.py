import requests

# image_url = 'https://scontent.fkul4-4.fna.fbcdn.net/v/t39.30808-6/321126908_492620782857665_2341688839928558899_n.jpg?stp=dst-jpg_p843x403&_nc_cat=110&ccb=1-7&_nc_sid=8bfeb9&_nc_ohc=byRoUtDIfs0AX8qb5y8&tn=ejNr4DCOLOPgnh5f&_nc_ht=scontent.fkul4-4.fna&oh=00_AfDG_ISo9Wpom_Mb6HhQSRVdfKbSo_724eRY5wSsg931XA&oe=63AFD7F3'

# img_data = requests.get(image_url).content
# with open('image_name.jpg', 'wb') as handler:
#     handler.write(img_data)

def send_data(type, data):
            
    if type == 'data':
        # API link for data insert
        url = 'https://onesplatform.com/api_insert_data.php'
        print('Sending Data through API')
        try:
            x = requests.post(url, json=data)
            if x.text not in ['2','3','4']:
                print('Success inserted data:', x.text)
                return x.text
            elif x.text == '2':
                print('Response: 2, Failed to Insert Data')
            elif x.text == '3':
                print('Response: 3, Incomplete Data POST')
            elif x.text == '4':
                print('Response: 4, Invalid API Key')
        except:
            pass

    elif type == 'image':
        # API link for inserting image
        image_url = 'https://onesplatform.com/api_insert_image.php'
        try:
            x = requests.post(image_url, json=data)
            if x.text not in ['2','3','4']:
                print('Images instered successfully')
            elif x.text == '2':
                print('Response: 2, Failed to Insert Data')
            elif x.text == '3':
                print('Response: 3, Incomplete Data POST')
            elif x.text == '4':
                print('Response: 4, Invalid API Key')
        except:
            pass

    return 'unsuccessful'

obj_img = {
    'data_ID':'D1672205675',
    'img_url':'https://i.ibb.co/7pfSmMN/2177ab6858fa.png',
    'type': '2',
    'APIKEY': 'RARazPnC2z47HB1uw962y8uI9AL5nDCQdXzDgqwgMt'
}

send_data('image', obj_img)