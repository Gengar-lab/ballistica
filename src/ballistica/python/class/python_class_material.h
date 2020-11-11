// Released under the MIT License. See LICENSE for details.

#ifndef BALLISTICA_PYTHON_CLASS_PYTHON_CLASS_MATERIAL_H_
#define BALLISTICA_PYTHON_CLASS_PYTHON_CLASS_MATERIAL_H_

#include "ballistica/core/object.h"
#include "ballistica/python/class/python_class.h"

namespace ballistica {

class PythonClassMaterial : public PythonClass {
 public:
  static auto type_name() -> const char* { return "Material"; }
  static void SetupType(PyTypeObject* obj);
  static auto Check(PyObject* o) -> bool {
    return PyObject_TypeCheck(o, &type_obj);
  }
  static PyTypeObject type_obj;

  auto GetMaterial(bool doraise = true) const -> Material* {
    Material* m = material_->get();
    if ((!m) && doraise) throw Exception("Invalid Material");
    return m;
  }

 private:
  static bool s_create_empty_;
  static PyMethodDef tp_methods[];
  static auto tp_new(PyTypeObject* type, PyObject* args, PyObject* keywds)
      -> PyObject*;
  static void Delete(Object::Ref<Material>* m);
  static void tp_dealloc(PythonClassMaterial* self);
  static auto tp_getattro(PythonClassMaterial* self, PyObject* attr)
      -> PyObject*;
  static auto tp_setattro(PythonClassMaterial* self, PyObject* attr,
                          PyObject* val) -> int;
  static auto tp_repr(PythonClassMaterial* self) -> PyObject*;
  static auto AddActions(PythonClassMaterial* self, PyObject* args,
                         PyObject* keywds) -> PyObject*;
  static auto Dir(PythonClassMaterial* self) -> PyObject*;
  Object::Ref<Material>* material_;
};

}  // namespace ballistica

#endif  // BALLISTICA_PYTHON_CLASS_PYTHON_CLASS_MATERIAL_H_
