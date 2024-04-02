from abc import ABC, abstractmethod

class ScormScraperABC(ABC):
    @abstractmethod
    def parser(self, driver):
        pass
    

    # is validate method
    @abstractmethod
    def validate(self, driver):
        pass