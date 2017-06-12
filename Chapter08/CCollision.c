#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "Python.h"

bool LineIntersection2D(float Ax, float Ay, float Bx, float By, float Cx, float Cy, float Dx, float Dy, float* dist) {
	float Bx_Ax = Bx-Ax;
	float Dy_Cy = Dy-Cy;
	float By_Ay = By-Ay;
	float Dx_Cx = Dx-Cx;
	float Ay_Cy = Ay-Cy;
	float Ax_Cx = Ax-Cx;

	*dist = 0.0;
	float Denominator = (Bx_Ax*Dy_Cy - By_Ay*Dx_Cx);

	if (-0.000005<Denominator && Denominator<0.000005){
		return false;
	}

	float rNumerator  = Ay_Cy*Dx_Cx - Ax_Cx*Dy_Cy;
	float sNumerator  = Ay_Cy*Bx_Ax - Ax_Cx*By_Ay;

	float r = rNumerator / Denominator;
	float s = sNumerator / Denominator;

	if(0<=r && r<=1.0 && 0<=s && s<=1.0){
		*dist = r;
		return true;
	}else{
		return false;
	}
}

static PyObject *
CCollision_LineIntersection2D(PyObject *self, PyObject *args) {
    int res;
    float Ax, Ay, Bx, By, Cx, Cy, Dx, Dy, dist;
    bool returnV;
    PyObject* retval;
    //从输入参数解析出两个整型数据
    res = PyArg_ParseTuple(args, "fffffffff", &Ax, &Ay, &Bx, &By, &Cx, &Cy, &Dx, &Dy, &dist);
    if (!res) {
        return NULL;
    }
    //调用C函数进行实际操作
    returnV = LineIntersection2D(Ax, Ay, Bx, By, Cx, Cy, Dx, Dy, &dist);
    //将结果转换成一个python对象返回
    retval= (PyObject *)Py_BuildValue("b", returnV);
    return retval;
}

static PyMethodDef
CCollisionMethods[] = {
    {"LineIntersection2D", CCollision_LineIntersection2D, METH_VARARGS},
    {NULL, NULL},
};

void initCCollision() {
    Py_InitModule("CCollision", CCollisionMethods);
}