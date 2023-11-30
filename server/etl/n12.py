from pydantic import BaseModel, Field
from .common import EtlData
from typing import Optional
import bs4
from db.models import Document

class N12Document(EtlData):

    class Category(BaseModel):
        id: int = Field(..., alias="id")
        name: str = Field(..., alias="name")

    class App(BaseModel):
        id: int = Field(..., alias="id")
        name: str = Field(..., alias="name")
        domain: str = Field(..., alias="domain")

    class Location(BaseModel):
        lat: float = Field(..., alias="lat")
        lon: float = Field(..., alias="lon")

    item_id: int = Field(..., alias="item_id")
    event_type: str = Field(..., alias="event_type")
    header: str = Field(..., alias="header")
    address: str = Field(..., alias="address")
    # TODO clean the html tags
    content: str = Field(..., alias="content")
    contact_name: Optional[str] = Field(None, alias="contact_name")
    contact_email: Optional[str] = Field(None, alias="contact_email")
    contact_phone: Optional[str] = Field(None, alias="contact_phone")
    external_link: Optional[str] = Field(None, alias="external_link")
    report_link: Optional[str] = Field(None, alias="report_link")
    is_active: int = Field(..., alias="is_active")
    subcats: list[Category] = Field(..., alias="subcats")
    apps: list[App] = Field(..., alias="apps")
    cat: Category = Field(..., alias="cat")
    location: Location = Field(..., alias="location")

    @classmethod
    def from_list(cls, data: list[dict]) -> list["N12Document"]:
        MENTAL_HEALTH_CAT_ID = 98

        def item_condition(item: dict) -> bool:

            all_cat = [item["cat"]["id"]] + [subcat["id"] for subcat in item["subcats"]]

            return item["is_active"] == 1 and MENTAL_HEALTH_CAT_ID in all_cat

        def format_content(content: str) -> str:
            soup = bs4.BeautifulSoup(content, features="html.parser")
            return soup.get_text()

        output = []

        for item in data:
            if item_condition(item):
                item["content"] = format_content(item["content"])
                output.append(N12Document(**item))
            
        return output

    def into_document(self) -> "Document":
        
        contact_str = ""

        if self.contact_name is not None:
            contact_str += self.contact_name
        
        if self.contact_phone is not None:
            contact_str += f" {self.contact_phone}"

        if self.contact_email is not None:
            contact_str += f" {self.contact_email}"

        return Document(
            extrnal_id=str(self.item_id),
            title=self.header,
            content=self.content,
            contact=contact_str,
            link=self.external_link,
        )