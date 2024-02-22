from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse,HttpResponse
import subprocess
from .db_connection import db
import json
from .functions.verifyUser import verify_token

# Create your views here.
def home(request):
    return HttpResponse("Welcome to my Django API")

@api_view(['GET'])
def get_data(request, id):
    try:
        if not verify_token(request):
            return JsonResponse({'message': 'Unauthorized'}, status=401)
        # Tìm giỏ hàng của người dùng
        cart = db['usercarts'].find_one({'username': id})
        if not cart or not cart.get('carts') or len(cart['carts']) == 0:
            return JsonResponse({'data': []}, status=200)
        
        # Lấy danh sách các giao dịch từ cơ sở dữ liệu
        list_trans_cursor = db['transactions'].find({}, {'listProduct': 1, '_id': 0})
        list_trans = [trans['listProduct'] for trans in list_trans_cursor]

        # Lấy danh sách sản phẩm từ giỏ hàng
        list_product = [item['productID'] for item in cart['carts']]
        path_to_file = 'myapp/fin_and_agrawal.py'
        result = subprocess.check_output(['python', path_to_file, json.dumps(list_trans),json.dumps(list_product)], universal_newlines=True)
        # Kết quả có thể được xử lý hoặc trả về trực tiếp
        # Trong ví dụ này, chúng ta trả về kết quả như một JSON response
        format_result = json.loads(result)
        if(len(format_result)):
            consequentProduct = format_result[0][format_result[0].index("==>") + 1]
            recommendProduct = db['products'].find_one({'productID': consequentProduct})
            data = {
                'data': json.loads(json.dumps(recommendProduct, default=str)),
            }
            return JsonResponse(data,status=200)
        else:
            return JsonResponse({'data':[]},status=200)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)