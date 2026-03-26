"""
Monkeypatch for pydantic to support Python 3.14 type hints
Fixes: "unable to infer type for attribute" error with Optional fields
"""
import sys
from typing import Optional, get_origin, get_args

# Patch pydantic's ModelField before anything imports FastAPI
import pydantic.fields as pydantic_fields
original_infer = pydantic_fields.ModelField.infer

@classmethod
def patched_infer(cls, name, value, annotation, class_validators, config):
    """
    Patched infer method that handles Optional[] types in Python 3.14
    """
    try:
        # Try original inference
        return original_infer(name=name, value=value, annotation=annotation, 
                             class_validators=class_validators, config=config)
    except Exception as e:
        if "unable to infer type" in str(e) and annotation and hasattr(annotation, '__origin__'):
            # Handle Optional[T] which is Union[T, None]
            origin = get_origin(annotation)
            args = get_args(annotation)
            
            if origin is not None:
                # Convert Union types to a simpler representation
                if hasattr(origin, '__name__') and 'Union' in str(origin):
                    # This is Optional or Union
                    non_none_types = [arg for arg in args if arg is not type(None)]
                    if non_none_types:
                        # Use the first non-None type
                        new_annotation = non_none_types[0]
                        return original_infer(name=name, value=value, annotation=new_annotation,
                                            class_validators=class_validators, config=config)
        raise

pydantic_fields.ModelField.infer = patched_infer
