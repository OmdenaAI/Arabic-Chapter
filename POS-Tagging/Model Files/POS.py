from POS_SVM import POS_SVM
from POS_BILSTM import POS_BILSTM

class POS:
    def __init__(self,model = 'SVM'):
        if model == 'SVM':
            self.model = POS_SVM()
            self.predict_func = self.model.classify
        elif model == 'BILSTM':
            self.model = POS_BILSTM()
            self.predict_func = self.model.classify
        else:
            return 'Incorrect Model Name(Model name should be either SVM or BILSTM)'
    def predict(self,sent):
        return self.predict_func(sent)