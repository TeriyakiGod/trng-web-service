import asyncio
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from asgiref.sync import async_to_sync
from . import rand
from datetime import datetime

## @brief This view returns a json object with a list of random integers and a timestamp.
# @param request HTTP request object.
# @return HTTP response object with either a list of random integers or an error message.
@api_view(['GET'])
def get_rand_int(request: Request):
    data = None
    status = 200

    n = int(request.query_params.get('n', 1))
    if n <= 0:
        data = {"error": "Invalid n. Must be greater than 0"}
        status = 400
    elif n > 10000:
        data = {"error": "Invalid n. Must be less than or equal to 10000"}
        status = 400
    else:
        min = int(request.query_params.get('min', 0)) # TODO: Determine the possible range
        max = int(request.query_params.get('max', 100))
        if min > max:
            data = {"error": "Invalid parameters. min must be less than or equal to max."}
            status = 400
        elif min > 1000000000 or max > 1000000000 or min < -1000000000 or max < -1000000000:
            data = {"error": "Invalid parameters. min and max must be between -1000000000 and 1000000000."}
            status = 400
        else:
            repeat = request.query_params.get('repeat', 'True') != 'False'
            if not repeat and n > (max - min + 1):
                data = {"error": "Invalid parameters. n must be less than or equal to the length of the range, when repeat is false."}
                status = 400
            else:
                try:
                    values = async_to_sync(rand.get_int)(n, min, max)
                except asyncio.TimeoutError:
                    data = {"error": "ERROR: The service is currently unavailable. Please try again later."}
                    status = 503
                timestamp = datetime.now().isoformat()
                data = {"values": values, "timestamp": timestamp}
    return Response(data, status=status)

## @brief This view returns a json object with a list of random floats and a timestamp.
# @param request HTTP request object.
# @return HTTP response object with either a list of random floats or an error message.
@api_view(['GET'])
def get_rand_float(request: Request):
    data = None
    status = 200

    n = int(request.query_params.get('n', 1))
    if n <= 0:
        data = {"error": "Invalid n. Must be greater than 0"}
        status = 400
    elif n > 1024:
        data = {"error": "Invalid n. Must be less than or equal to 1024"}
        status = 400
    else:
        p = int(request.query_params.get('precision', 2))
        if p < 1:
            data = {"error": "Invalid precision. Must be greater than or equal to 1"}
            status = 400
        elif p > 10:
            data = {"error": "Invalid precision. Must be less than or equal to 15"}
            status = 400
        else:
            try:
                values = async_to_sync(rand.get_float)(n, p)
            except asyncio.TimeoutError:
                data = {"error": "ERROR: The service is currently unavailable. Please try again later."}
                status = 503
            timestamp = datetime.now().isoformat()
            data = {"values": values, "timestamp": timestamp}
    return Response(data, status=status)

## @brief This view returns a json object with a list of random bytes and a timestamp.
# @param request HTTP request object.
# @return HTTP response object with either a list of random bytes or an error message.
@api_view(['GET'])
def get_rand_bytes(request: Request):
    data = None
    status = 200

    n = int(request.query_params.get('n', 4))
    if n <= 0:
        data = {"error": "Invalid n. Must be greater than 0"}
        status = 400
    elif n > 1024:
        data = {"error": "Invalid n. Must be less than or equal to 1024"}
        status = 400
    else:
        f = str(request.query_params.get('f', 'h'))
        if f not in ['h', 'o', 'b', 'd', '']:
            data = {"error": "Invalid format. Must be one of ['h', 'o', 'b', 'd', '']"}
            status = 400
        else:
            try:
                values = async_to_sync(rand.get_bytes)(n, f)
            except asyncio.TimeoutError:
                data = {"error": "ERROR: The service is currently unavailable. Please try again later."}
                status = 503
            timestamp = datetime.now().isoformat()
            data = {"values": values, "timestamp": timestamp}
    return Response(data, status=status)

## @brief This view returns a json object with a list of random strings and a timestamp.
# @param request HTTP request object.
# @return HTTP response object with either a list of random strings or an error message.
@api_view(['GET'])
def get_rand_string(request: Request):
    data = None
    status = 200

    n = int(request.query_params.get('n', 4))
    if n <= 0:
        data = {"error": "Invalid n. Must be greater than 0"}
        status = 400
    elif n > 1024:
        data = {"error": "Invalid n. Must be less than or equal to 1024"}
        status = 400
    else:
        digits = request.query_params.get('digits', 'True') != 'False'
        letters = request.query_params.get('letters', 'True') != 'False'
        special = request.query_params.get('special', 'True') != 'False'
        repeat = request.query_params.get('repeat', 'True') != 'False'
        limit = (52 if letters else 0) + (10 if digits else 0) + (33 if special else 0)
        if not digits and not letters and not special:
            data = {"error": "Invalid parameters. At least one of digits, letters, or special must be true."}
            status = 400
        elif not repeat and n > limit:
            data = {"error": "Invalid parameters. n must be less than or equal to" + str(limit) + "with those options, when repeat is false."}
            status = 400
        else:
            try:
                values = async_to_sync(rand.get_string)(n, digits, letters, special, repeat)
            except asyncio.TimeoutError:
                data = {"error": "ERROR: The service is currently unavailable. Please try again later."}
                status = 503
            timestamp = datetime.now().isoformat()
            data = {"values": values, "timestamp": timestamp}
    return Response(data, status=status)
      
## @brief This view returns a json object with a random sequence in range and a timestamp.
# @param request HTTP request object.
# @return HTTP response object with either a list of random integers or an error message.  
@api_view(['GET'])
def get_rand_sequence(request: Request):
    data = None
    status = 200

    min = int(request.query_params.get('min', 0))
    max = int(request.query_params.get('max', 100))
    if min > max:
        data = {"error": "Invalid parameters. min must be less than or equal to max."}
        status = 400
    elif min > 1000000000 or max > 1000000000 or min < -1000000000 or max < -1000000000:
        data = {"error": "Invalid parameters. min and max must be between -1000000000 and 1000000000."}
        status = 400
    else:
        try:
            values = async_to_sync(rand.get_sequence)(min, max)
        except asyncio.TimeoutError:
            data = {"error": "ERROR: The service is currently unavailable. Please try again later."}
            status = 503
        timestamp = datetime.now().isoformat()
        data = {"values": values, "timestamp": timestamp}
    return Response(data, status=status)

## @brief This view returns a json object with a list of random coin flips and a timestamp.
# @param request HTTP request object.
# @return HTTP response object with either a list of random coin flips or an error message.
@api_view(['GET'])
def get_rand_coin(request: Request):
    data = None
    status = 200

    n = int(request.query_params.get('n', 2))
    if n <= 0:
        data = {"error": "Invalid n. Must be greater than 0"}
        status = 400
    elif n > 1024:
        data = {"error": "Invalid n. Must be less than or equal to 1024"}
        status = 400
    else:
        try:
            values = async_to_sync(rand.get_coin_flips)(n)
        except asyncio.TimeoutError:
            data = {"error": "ERROR: The service is currently unavailable. Please try again later."}
            status = 503
        timestamp = datetime.now().isoformat()
        data = {"values": values, "timestamp": timestamp}
    return Response(data, status=status)

## @brief This view returns a json object with a list of random dice rolls and a timestamp.
# @param request HTTP request object.
# @return HTTP response object with either a list of random dice rolls or an error message.
@api_view(['GET'])
def get_rand_dice(request: Request):
    data = None
    status = 200

    n = int(request.query_params.get('n', 2))
    m = int(request.query_params.get('m', 6))
    if n <= 0:
        data = {"error": "Invalid n. Must be greater than 0"}
        status = 400
    elif n > 1024:
        data = {"error": "Invalid n. Must be less than or equal to 1024"}
        status = 400
    elif m < 2:
        data = {"error": "Invalid m. Must be greater than or equal to 2"}
        status = 400
    elif m > 100:
        data = {"error": "Invalid m. Must be less than or equal to 100"}
        status = 400
    else:
        try:
            values = async_to_sync(rand.get_dice_rolls)(n, m)
        except asyncio.TimeoutError:
            data = {"error": "ERROR: The service is currently unavailable. Please try again later."}
            status = 503
        timestamp = datetime.now().isoformat()
        data = {"values": values, "timestamp": timestamp}
    return Response(data, status=status)

## @brief This view returns a json object with a list of random lotto tickets and a timestamp.
# @param request HTTP request object.
# @return HTTP response object with either a list of random lotto tickets or an error message.
@api_view(['GET'])
def get_rand_lotto(request: Request):
    data = None
    status = 200

    n = int(request.query_params.get('n', 1))
    if n <= 0:
        data = {"error": "Invalid n. Must be greater than 0"}
        status = 400
    elif n > 1024:
        data = {"error": "Invalid n. Must be less than or equal to 1024"}
        status = 400
    else:
        try:
            values = async_to_sync(rand.get_lotto)(n)
        except asyncio.TimeoutError:
            data = {"error": "ERROR: The service is currently unavailable. Please try again later."}
            status = 503
        timestamp = datetime.now().isoformat()
        data = {"values": values, "timestamp": timestamp}
    return Response(data, status=status)