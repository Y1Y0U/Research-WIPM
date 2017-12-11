import os
import re
import numpy as np
import matplotlib.pyplot as plt

class Dataset1D(object):
	"""
	Read raw 1D FID in BRUKER convention and reform into an array of time dependent complex numbers
	FID plotting is possible
	"""

	def __init__(self, dataset_dir_path, exp_no, proc_no,pos_shift=138):
		'''
		Requires the absolute directory path of 1D experiment, number of experiment. 
		The number of processing is also needed, provided that the processed data is required
		'''
		self.ds_dir_path = dataset_dir_path
		self.exp_no = exp_no
		self.proc_no = proc_no
		self.cmplx_fid = self.mkCplxFid(pos_shift)
		self.proc_spec = self.getProcSpec()

	def getFid(self):
		try:
			fid_dir_path = self.ds_dir_path + str(self.exp_no)
			os.chdir(fid_dir_path)
			temp = np.fromfile('fid', dtype=np.int32)
		except IOError:
			print('FID file does not exist')
		return temp

	def mkCplxFid(self,pos_shift):
		temp = self.getFid()
		temp = np.concatenate((temp[pos_shift:], np.zeros(pos_shift)), axis=0)
		cmplx_fid = temp[0::2] + 1j * temp[1::2]
		return cmplx_fid

	def plotFid(self, part='r',pos_shift=138):
		'''
		plot either the real part ('r') or the imaginary part ('i') of the complex FID
		'''
		if part == 'r':
			plt.plot(self.cmplx_fid.real)
		elif part == 'i':
			plt.plot(self.cmplx_fid.imag)
		plt.show()
		
	def plotFT(self):
		temp = np.fft.fft(self.cmplx_fid)
		temp = np.fft.fftshift(temp)
		plt.plot(temp)
		plt.show()

	def getProcSpec(self):
		try:
			proc_dir_path = self.ds_dir_path + str(self.exp_no) + '/pdata/' + str(self.proc_no)
			os.chdir(proc_dir_path)
			temp = np.fromfile('1r', dtype=np.int32)
		except IOError:
			print('Processed spectrum does not exist')
		return temp		

	def plotProcSpec(self):
		temp = self.getProcSpec()
		plt.plot(temp)
		plt.show()

class RandSensing(object):
	"""
	Sparsity Adaptive Matching Persuit
	
	According to the theory of Compressed Sensing, we have:
		
		y_(Mx1) = Phi(MxN) * x(Nx1)
		y : M-entry-vector of measured data
		Phi : MxN-matrix of measuring matrix
		x : N-entry-vector of original data
		
	First we construct a random sensing matrix(RSM), where N equals to the length of complex FID from experimental dataset. M, the length of the array of measurement, has a theoretical lower limit, which can be obtained from the Theorem of Measurement Bound:
		
		M >= C*k*log(n/k), 
		C=\frac{1}{2(1+\sqrt{24})} = 0.28,
		k = nbr of non-zero freqs
	
	We know already the value of k in a deterministic way. So we first set k = 2, then m > 0.28*2*4.21 = 2.35.
	In practice, we adopt in the first attempts M = 4k, sparsity 12.5%
	
	
	
	"""
	
	def __init__(self, original_dataset, sparsity=0.125):
		self.len_original = len(original_dataset.proc_spec)
		self.sparsity = sparsity
		self.len_measure = np.floor(self.len_original*self.sparsity)
		self.gaussianRSM = self.mkGaussianRSM()
		self.g_measured_data = np.dot(self.gaussianRSM,original_dataset.proc_spec)
	
	def mkGaussianRSM(self):
		temp = np.random.normal(0, 1.0/self.len_measure, self.len_measure*self.len_original)
		temp = np.reshape(temp, (-1, self.len_original))
		return temp

	def mkBernoulliRSM(self):
		temp = np.random.binomial(1,0.5, self.len_measure*self.len_original)
		temp = np.reshape(temp, (-1, self.len_original))
		return temp

if __name__ == "__main__":

#	dataset_dir_path='C:/Bruker/TopSpin3.5.b.91pl7/examdata/NMR Data/xj-20171117/'
	dataset_dir_path='C:/NMR Spectra/156574_0001csol/'
	exp_no = 10  
	proc_no = 1
	test_dataset = Dataset1D(dataset_dir_path, exp_no, proc_no,pos_shift=125)
#	test_dataset.plotFid()
#	test_dataset.plotProcSpec()
	
	
	test_RS = RandSensing(test_dataset)
	
#	plt.plot(test_RS.g_measured_data)
#	plt.show()

	print(np.random.binomial(1, 0.5, len_measure*self.len_original))
