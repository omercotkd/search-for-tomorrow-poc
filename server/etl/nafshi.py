from pydantic import BaseModel, Field
from .common import EtlData
from db.models import Document
from typing import Optional

class NafshiDocument(EtlData):

    class DateField(BaseModel):
        date: str = Field(..., alias="$date")

    id: str = Field(..., alias="_id")
    service_type: Optional[str] = Field(None, alias="serviceType")
    location: Optional[str] = Field(None, alias="location")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    tags_ages: list[str] = Field(default_factory=list, alias="tagsAges")
    service_orientation_tags: list[str] = Field(default_factory=list, alias="serviceOrientationTags")
    created_date: DateField = Field(..., alias="_createdDate")
    service_name: Optional[str] = Field(None, alias="serviceName")
    added_by: Optional[str] = Field(None, alias="addedBy")
    organization_name: Optional[str] = Field(None, alias="organizationName")
    updated_date: DateField = Field(..., alias="_updatedDate")
    paid_service: Optional[bool] = Field(None, alias="paidService")
    langs_tags: list[str] = Field(default_factory=list, alias="langsTags")
    service_orientation: Optional[str] = Field(None, alias="serviceOrientation")
    service_type_11: list[str] = Field(default_factory=list, alias="serviceType11")
    status: Optional[str] = Field(None, alias="status")
    org_type_tags_1: list[str] = Field(default_factory=list, alias="orgTypeTags1")
    service_description: Optional[str] = Field(None, alias="serviceDescription")
    location_1: list[str] = Field(default_factory=list, alias="location1")
    tags_population_type: list[str] = Field(default_factory=list, alias="tagsPopulationType")
    target_audience_tags: list[str] = Field(default_factory=list, alias="targetAudienceTags")
    service_emotion: Optional[str] = Field(None, alias="serviceEmotion")
    orthodox: Optional[str] = Field(None, alias="orthodox")
    org_type: Optional[str] = Field(None, alias="orgType")
    service_orientation_tags_1: list[str] = Field(default_factory=list, alias="serviceOrientationTags1")
    service_link: Optional[str] = Field(None, alias="serviceLink")


    @classmethod
    def from_list(cls, data: list[dict]) -> list["EtlData"]:

        output = []

        for i, item in enumerate(data):
            try:
                output.append(NafshiDocument(**item))
            except Exception as e:
                print(f"Failed to parse item {i}")
                print(e)

        return output

    def into_document(self) -> "Document":

        contact_str = ""

        content_str = self.service_description

        if self.phone_number:
            contact_str += f"טלפון: {self.phone_number}"

        if self.location:
            content_str += f"\n\nמיקום: {self.location}"

        return Document(
            extrnal_id=self.id,
            title=self.service_name,
            content=self.service_description,
            contact=self.phone_number,
            link=self.service_link,
        )

