# services/response.py

from typing import List, Optional, Dict
from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from models.response import Response
from models.user import User
from schemas.response import ResponseCreate, ResponseOut

def create_response(data: ResponseCreate) -> ResponseOut:
    user =  User.objects(id=data.user_id).first()
    user_dict = user.to_mongo().to_dict()
    user_dict['id'] = str(user_dict['_id'])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    response = Response(
        id_link=str(uuid4()),
        status="PENDING",
        date=datetime.utcnow(),
        user_id = user
    )
    print(response.to_mongo().to_dict())
    response.save()
    response_dict = response.to_mongo().to_dict()
    response_dict['id'] = str(response_dict['_id'])
    response_dict['user_id'] = user_dict
    return ResponseOut.parse_obj(response_dict)

def get_response(id_link: str) -> Optional[ResponseOut]:
    response = Response.objects(id_link=id_link).first()
    
    if not response:
        return None
    response_dict = response.to_mongo().to_dict()
    response_dict['id'] = str(response_dict['_id'])
    user = response_dict['user_id']
    user =  User.objects(id=user).first()
    user_dict = user.to_mongo().to_dict()
    user_dict['id'] = str(user_dict['_id'])
    response_dict['user_id'] = user_dict
    return ResponseOut.parse_obj(response_dict)

def get_all_responses() -> List[ResponseOut]:
    responses = Response.objects.all()
    result = []
    for response in responses:
        response_dict = response.to_mongo().to_dict()
        response_dict['id'] = str(response_dict['_id'])
        user = response_dict['user_id']
        print("user_in =========> ", response_dict['user_id'])
        print("id", response_dict['id'])
        user =  User.objects(id=user).first()
        user_dict = user.to_mongo().to_dict()
        user_dict['id'] = str(user_dict['_id'])
        response_dict['user_id'] = user_dict
        result.append(ResponseOut.parse_obj(response_dict))
    return result

def update_response(id_link: str, data: Dict) -> Optional[ResponseOut]:
    response = Response.objects(id_link=id_link).first()
    if not response:
        return None

    status = data.get("status", response.status)
    content = data.get("content", None)

    if content:
        sorted_content = {k: content[k] for k in sorted(content.keys())}
        response.content = sorted_content

    response.status = status

    if status == "COMPLETED" and content:
        stats = {}
        letters = [key[0] for key in content.keys()]
        for letter in letters:
            total_keys = sum(1 for key in content.keys() if key.startswith(letter))
            true_keys = sum(1 for key in content.keys() if key.startswith(letter) and content[key] == True)
            stats[letter] = f"{true_keys}/{total_keys}"
        response.statistique = stats

    response.save()
    response_dict = response.to_mongo().to_dict()
    response_dict['id'] = str(response_dict['_id'])
    user = response_dict['user_id']
    user =  User.objects(id=user).first()
    user_dict = user.to_mongo().to_dict()
    user_dict['id'] = str(user_dict['_id'])
    response_dict['user_id'] = user_dict
    return ResponseOut.parse_obj(response_dict)

def delete_response(response_id: str) -> Optional[ResponseOut]:
    response = Response.objects(id=response_id).first()
    if not response:
        return None
    response.delete()
    response_dict = response.to_mongo().to_dict()
    response_dict['id'] = str(response_dict['_id'])
    user = response_dict['user_id']
    user =  User.objects(id=user).first()
    user_dict = user.to_mongo().to_dict()
    user_dict['id'] = str(user_dict['_id'])
    response_dict['user_id'] = user_dict
    return ResponseOut.parse_obj(response_dict)

def update_response_personality(response_id: str, id_personality: int) -> Optional[ResponseOut]:
    response = Response.objects(id=response_id).first()
    if not response:
        return None
    response.update(id_personality=id_personality)
    response.reload()
    response_dict = response.to_mongo().to_dict()
    response_dict['id'] = str(response_dict['_id'])
    user = response_dict['user_id']
    user =  User.objects(id=user).first()
    user_dict = user.to_mongo().to_dict()
    user_dict['id'] = str(user_dict['_id'])
    response_dict['user_id'] = user_dict
    return ResponseOut.parse_obj(response_dict)
