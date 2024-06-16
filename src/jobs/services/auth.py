from abc import ABC, abstractmethod
from dataclasses import dataclass
from ..models.database import Session


@dataclass
class AuthService(ABC):
    """
    Abstract class for service classes that need to implement authentication.
    """

    session: Session = Session()

    @abstractmethod
    def authenticate(self):
        """
        Abstract method for authenticating an entity.
        """
        pass
