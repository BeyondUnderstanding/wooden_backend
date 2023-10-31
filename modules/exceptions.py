from fastapi.exceptions import HTTPException

NOT_IMPLEMENTED = HTTPException(500, {'error': 'Not implemented yet'})