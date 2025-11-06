#Importing annotations for future compatibility
from __future__ import annotations as _annotations

#Importing necessary libraries and modules
from dataclasses import dataclass, field
from pathlib import Path

from utils.agents import *
from utils.evaluators import *

from groq import BaseModel

from pydantic_graph import (
    BaseNode,
    End,
    Graph,
    GraphRunContext,
)

from pydantic_graph.persistence.file import FileStatePersistence

from rich.prompt import Prompt

from pydantic_ai import Agent, format_as_xml
from pydantic_ai.messages import ModelMessage


