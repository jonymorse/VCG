from abc import ABC, abstractmethod

class Exp(ABC):
    @abstractmethod
    def print(self):
        pass
    
    @abstractmethod
    def substitute(self, var, exp):
        """Substitute all occurrences of variable var with expression exp
        
        Args:
            var (str): Variable name to be substituted
            exp (Exp): Expression to substitute with
            
        Returns:
            Exp: A new expression with the substitution applied
        """
        pass