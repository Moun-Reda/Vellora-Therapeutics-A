from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal, Union


class ToolAction(BaseModel):
    type: Literal["tool_call"]
    action: Literal[
        "get_disease",
        "get_drug",
        "get_possible_drugs",
        "check_allergy",
        "check_contraindications",
        "check_interactions",
        "get_dosage",
        "get_alternative",
    ]
    arguments: Dict


class FinalAnswer(BaseModel):
    type: Literal["final_answer"]

    drug: str
    active_ingredient: str
    dosage: str
    warnings: List[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    response: Union[ToolAction, FinalAnswer]