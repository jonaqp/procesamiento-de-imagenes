''' Este archivo se debe llamar Mascaras.py, por x razon git lo cambia a minusulas. '''
class Mascaras():
	def __init__(self):
		self.arr_sobelX = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
		self.arr_sobelY = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

		self.arr_robertsX = [[0, 1], [-1, 0]]
		self.arr_robertsY = [[1, 0], [0, -1]]

		self.arr_prewittX = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
		self.arr_prewittY = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]



		
