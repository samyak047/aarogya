from sklearn.externals import joblib
import numpy as np

class Test():
	logreg = joblib.load('./model.pkl')

	def test(self, arr):
		arr = np.array(arr).reshape(1, -1)
		return self.logreg.predict_proba(arr)