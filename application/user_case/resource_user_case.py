from domain.resource import Resource
from enum import Enum

class ResourceUserCase:
    def __init__(self,diamond:int=0, sapphire:int=0, emerald:int=0,ruby:int=0, onyx:int=0,gold:int=0,resource:Resource=None)->None:
        self.diamond=diamond
        self.sapphire=sapphire
        self.emerald =emerald
        self.ruby =ruby
        self.onyx = onyx
        self.gold =gold
        if resource:
            self.domain_to_usercase(resource)
        
    def domain_to_usercase(self,resource:Resource)->None:
        self.diamond = resource.diamond       
        self.sapphire = resource.sapphire      
        self.emerald = resource.emerald      
        self.ruby = resource.ruby      
        self.onyx = resource.onyx      
        self.gold = resource.gold  

    def usercase_to_domain(self)->Resource:
        return Resource(self.diamond,self.sapphire,self.emerald,self.ruby,self.onyx,self.gold)
    
    @classmethod
    def to_usercase(cls,diamond, sapphire, emerald,ruby, onyx,gold=0)->"ResourceUserCase":
        return cls(diamond, sapphire, emerald,ruby, onyx,gold)  


    @classmethod
    def map_from_json(cls, json_data)->"ResourceUserCase":
        return cls(json_data['diamond'],json_data['sapphire'],json_data['emerald'],json_data['ruby'],json_data['onyx'],json_data['gold'])
        
    def to_dict_card(self)->dict:
        return{
            "diamond":self.diamond,
            "sapphire":self.sapphire,
            "emerald":self.emerald,
            "ruby":self.ruby,
            "onyx":self.onyx
        }

class TokenUserCase(Enum):
    diamond = "diamond"#鑽石    
    sapphire = "sapphire"#藍寶石
    emerald = "emerald"#綠寶石
    ruby = "ruby"#紅寶石
    onyx = "onyx"#瑪瑙
    gold = "gold"#黃金
