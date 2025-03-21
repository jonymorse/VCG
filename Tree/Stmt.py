from abc import ABC, abstractmethod
from Tree import Exp

class Stmt(ABC):
    @abstractmethod
    def wp(self, post):
        """Calculate the weakest precondition for this statement.
        
        Args:
            post (Exp): Post condition
            
        Returns:
            Exp: The weakest precondition
        """
        pass