# services/response.py

from typing import List, Optional, Dict
from uuid import uuid4
from datetime import datetime
from models.response import Response
from schemas.response import ResponseCreate, ResponseUpdate, ResponseOut

def create_response(data: ResponseCreate) -> ResponseOut:
    response = Response(
        id_link=str(uuid4()),
        status="PENDING",
        date=datetime.utcnow(),
        **data.dict()
    )
    response.save()
    response_dict = response.to_mongo().to_dict()
    response_dict['id'] = str(response_dict['_id'])
    return ResponseOut.parse_obj(response_dict)

def get_response(response_id: str) -> Optional[ResponseOut]:
    response = Response.objects(id=response_id).first()
    if not response:
        return None
    response_dict = response.to_mongo().to_dict()
    response_dict['id'] = str(response_dict['_id'])
    return ResponseOut.parse_obj(response_dict)

def get_all_responses() -> List[ResponseOut]:
    responses = Response.objects.all()
    result = []
    for response in responses:
        response_dict = response.to_mongo().to_dict()
        response_dict['id'] = str(response_dict['_id'])
        result.append(ResponseOut.parse_obj(response_dict))
    return result

def update_response(response_id: str, data: Dict) -> Optional[ResponseOut]:
    response = Response.objects(id=response_id).first()
    if not response:
        return None

    status = data.get("status", response.status)
    content = data.get("content")

    if content:
        sorted_content = {k: content[k] for k in sorted(content.items(), lambda x : x[1])}
        response.content = sorted_content

    response.status = status

    if status == "COMPLETED" and content:
        stats = {}
        letters = {key[0] for key in content.keys()}
        for letter in letters:
            total_keys = sum(1 for key in content.keys() if key.startswith(letter))
            true_keys = sum(1 for key in content.keys() if key.startswith(letter) and content[key] == "true")
            stats[letter] = f"{true_keys}/{total_keys}"
        response.id_statistique = stats

    response.save()
    response_dict = response.to_mongo().to_dict()
    response_dict['id'] = str(response_dict['_id'])
    return ResponseOut.parse_obj(response_dict)

def delete_response(response_id: str) -> Optional[ResponseOut]:
    response = Response.objects(id=response_id).first()
    if not response:
        return None
    response.delete()
    response_dict = response.to_mongo().to_dict()
    response_dict['id'] = str(response_dict['_id'])
    return ResponseOut.parse_obj(response_dict)

def update_response_personality(response_id: str, id_personality: int) -> Optional[ResponseOut]:
    response = Response.objects(id=response_id).first()
    if not response:
        return None
    response.update(id_personality=id_personality)
    response.reload()
    response_dict = response.to_mongo().to_dict()
    response_dict['id'] = str(response_dict['_id'])
    return ResponseOut.parse_obj(response_dict)
