from pydantic import BaseModel,Field
class review(BaseModel):
    approved:bool=Field(
        description="Set to True ONLY if the post is perfectly ready to publish. False otherwise."
    )
    improvement:str=Field(description="If is_approved is False, provide detailed feedback on what needs to be improved. If True, leave empty.")