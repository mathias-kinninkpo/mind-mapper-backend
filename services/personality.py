# services/personality.py

from typing import List, Optional
from mongoengine import Document
from models.personality import Personality
from schemas.personality import PersonalityCreate, PersonalityUpdate, PersonalityResponse

def create_personality(data: PersonalityCreate) -> PersonalityResponse:
    personality = Personality(**data.dict())
    personality.save()
    personality_dict = personality.to_mongo().to_dict()
    personality_dict['id'] = str(personality_dict['_id'])
    return PersonalityResponse.parse_obj(personality_dict)

def get_personality(personality_id: str) -> Optional[PersonalityResponse]:
    personality = Personality.objects(id=personality_id).first()
    if not personality:
        return None
    personality_dict = personality.to_mongo().to_dict()
    personality_dict['id'] = str(personality_dict['_id'])
    return PersonalityResponse.parse_obj(personality_dict)

def get_all_personalities() -> List[PersonalityResponse]:
    personalities = Personality.objects.all()
    result = []
    for personality in personalities:
        personality_dict = personality.to_mongo().to_dict()
        personality_dict['id'] = str(personality_dict['_id'])
        result.append(PersonalityResponse.parse_obj(personality_dict))
    return result

def update_personality(personality_id: str, data: PersonalityUpdate) -> Optional[PersonalityResponse]:
    personality = Personality.objects(id=personality_id).first()
    if not personality:
        return None
    personality.update(**data.dict())
    personality.reload()
    personality_dict = personality.to_mongo().to_dict()
    personality_dict['id'] = str(personality_dict['_id'])
    return PersonalityResponse.parse_obj(personality_dict)

def delete_personality(personality_id: str) -> Optional[PersonalityResponse]:
    personality = Personality.objects(id=personality_id).first()
    if not personality:
        return None
    personality.delete()
    personality_dict = personality.to_mongo().to_dict()
    personality_dict['id'] = str(personality_dict['_id'])
    return PersonalityResponse.parse_obj(personality_dict)
