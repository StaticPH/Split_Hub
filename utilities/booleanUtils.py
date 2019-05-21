extendedTruths = [1, '1', 't', 'true', 'y', 'yes']
extendedFalsehoods = [0, '0', 'f', 'false', 'n', 'no']
extendedBools = extendedTruths + extendedFalsehoods

# Converts extendedBools to standard bools. Returns -1 for values not in extendedBools
# def correctBoolean (var):
# 	if (var == True) or (var in extendedTruths) or (str(var).capitalize() in extendedTruths):
# 		# print(str(var) + ' evaluated to: ' + str(True))
# 		return True
# 	elif (var == False) or (var in extendedFalsehoods) or (str(var).capitalize() in extendedFalsehoods):
# 		# print(str(var) + ' evaluated to: ' + str(False))
# 		return False
# 	else:
# 		#In some cases, the value assigned to a setting for 'True' is actually an integer greater than 1.
# 		#try to convert var to an int and check that, but don't mind it if the conversion fails
# 		print(var)
# 		try:
# 			if int(var) > 0: return True
# 			elif int(var) == 0: return False
# 		except:
# 			pass
# 		# print(str(var) + ' evaluated to: ' + str(-1) +'.\nValue should be corrected.')
# 		return -1

def isUsableAsBoolean(choice, allowAnyFloat: bool = False):
	try:
		choice = str(choice)
		if choice.lower() in extendedBools:
			return True
		# In some cases, the value assigned to a setting for 'True' is actually an integer greater than 1.
		# try to convert var to an int and check that, but don't mind it if the conversion fails
		elif allowAnyFloat:
			try:
				int(choice)
				return True
			except (TypeError, ValueError, BytesWarning):
				pass
	except TypeError:
		pass
	return False

def correctBoolean(choice: str, allowNonZeroAsTrue: bool = False, returnForInvalid = -1):
	choice = str(choice)  # In case a boolean or int mistakenly gets passed in
	if choice.lower() in ('true', 't', 'yes', 'y', '1'):
		return True
	elif choice.lower() in ('false', 'f', 'no', 'n', '0'):
		return False
	else:
		# print(var)
		try:
			if (int(choice) > 0) or (allowNonZeroAsTrue and int(choice) != 0):
				return True
			else:
				return False
		except (TypeError, ValueError, BytesWarning):
			print('String `' + choice + '` cannot be equated to a boolean value.')
			print('Returning ' + str(returnForInvalid))
			return returnForInvalid

def negate(boolean: bool): return not boolean

def isTruth(var): return correctBoolean(var)

def isFalsehood(var): return negate(correctBoolean(var))