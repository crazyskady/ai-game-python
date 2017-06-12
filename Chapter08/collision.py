# -*- coding: utf-8 -*-	
from C2DMatrix import SPoint

# Return: True means intersected, r is the distance

def LineIntersection2D_old(A, B, C, D):
	rDenominator = (B._x-A._x)*(D._y-C._y)-(B._y-A._y)*(D._x-C._x)
	rNumerator   = (A._y-C._y)*(D._x-C._x)-(A._x-C._x)*(D._y-C._y)	
	sDenominator = (B._x-A._x)*(D._y-C._y)-(B._y-A._y)*(D._x-C._x)
	sNumerator   = (A._y-C._y)*(B._x-A._x)-(A._x-C._x)*(B._y-A._y)

	if rDenominator == 0: # rDenominator == sDenominator
		# lines are parallel
		return False, 0

	r = (1.0) * rNumerator / rDenominator
	s = (1.0) * sNumerator / sDenominator
	#print rNumerator, sNumerator, rDenominator, r, s
	if 0<=r<=1.0 and 0<=s<=1.0:
		return True, r
	else:
		return False, 0

def LineIntersection2D_old1(A, B, C, D):
	Bx_Ax = B._x-A._x
	Dy_Cy = D._y-C._y
	By_Ay = B._y-A._y
	Dx_Cx = D._x-C._x
	Ay_Cy = A._y-C._y
	Dx_Cx = D._x-C._x
	Ax_Cx = A._x-C._x
	Dy_Cy = D._y-C._y

	Denominator = float(Bx_Ax*Dy_Cy - By_Ay*Dx_Cx)

	if -0.000005<Denominator<0.000005: # rDenominator == sDenominator
		# lines are parallel
		return False, 0

	rNumerator  = Ay_Cy*Dx_Cx - Ax_Cx*Dy_Cy
	sNumerator  = Ay_Cy*Bx_Ax - Ax_Cx*By_Ay

	r = rNumerator / Denominator
	s = sNumerator / Denominator
	#print rNumerator, sNumerator, Denominator, r, s
	if 0<=r<=1.0 and 0<=s<=1.0:
		return True, r
	else:
		return False, 0

def LineIntersection2D(Ax, Ay, Bx, By, Cx, Cy, Dx, Dy):
	Bx_Ax = Bx-Ax
	Dy_Cy = Dy-Cy
	By_Ay = By-Ay
	Dx_Cx = Dx-Cx
	Ay_Cy = Ay-Cy
	Dx_Cx = Dx-Cx
	Ax_Cx = Ax-Cx
	Dy_Cy = Dy-Cy

	Denominator = float(Bx_Ax*Dy_Cy - By_Ay*Dx_Cx)

	if -0.000005<Denominator<0.000005: # rDenominator == sDenominator
		# lines are parallel
		return False, 0

	rNumerator  = Ay_Cy*Dx_Cx - Ax_Cx*Dy_Cy
	sNumerator  = Ay_Cy*Bx_Ax - Ax_Cx*By_Ay

	r = rNumerator / Denominator
	s = sNumerator / Denominator
	#print rNumerator, sNumerator, Denominator, r, s
	if 0<=r<=1.0 and 0<=s<=1.0:
		return True, r
	else:
		return False, 0


if __name__ == '__main__':
	TestLines = [[(1,1), (2,2), (1,2), (2,1)],    # intersected: YES
				[(1,1), (2,2), (1,1), (2,2)],     # NO
				[(1,1), (2,2), (1,1), (2,1)],     # YES
				[(1,1), (2,2), (1,2), (2,3)],     # NO
				[(1,1), (2,2), (2,2), (3,3)],     # YES or NO???
				[(1,1), (2,2), (2,2), (3,4)]]     # YES	
	for points in TestLines:
		A = SPoint(points[0][0], points[0][1])
		B = SPoint(points[1][0], points[1][1])
		C = SPoint(points[2][0], points[2][1])
		D = SPoint(points[3][0], points[3][1])
		retCode, r = LineIntersection2D(A,B,C,D)
		intersected = "Yes" if retCode else "No"
		print "AB and CD is intersected?", intersected