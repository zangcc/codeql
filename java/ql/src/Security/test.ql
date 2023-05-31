import java

// 检测反射调用
from Class c, MethodAccess ma
where ma.getDeclaringType().equals(c)
and ma.getTarget().hasModifier("private")
and ma.getTarget().hasModifier("static")
and ma.getTarget().hasName("backdoor")
and not exists(DynamicCall dc |
  dc.getTarget().getName() = "invoke"
  and dc.getBase().equals(ma)
)

// 检查反射调用是否受到限制
from AccessControl ac, FieldAccess fa, MethodAccess ma2
where ac.getCaller().equals(ma2)
and (ac.getAccessed().equals(fa) or ac.getAccessed().equals(ma2))
and ac.isRestricted()

select ma.getTarget(), "Possible backdoor access via reflection"

// 检测注解调用
from Class c, Annotation a, Method m
where m.getDeclaringType().equals(c)
and a.getType().getName().endsWith("Backdoor")
and a.hasAnnotationParameter("value", m.getName())

select m, "Possible backdoor access via annotation"

// 检测动态代理调用
from Class c, MethodAccess ma3
where ma3.getDeclaringType().equals(c)
and ma3.getTarget().hasModifier("private")
and ma3.getTarget().hasModifier("static")
and ma3.getTarget().hasName("backdoor")
and exists(DynamicCall dc |
  dc.getTarget().getName() = "invoke"
  and dc.getBase().equals(ma3)
)

select ma3.getTarget(), "Possible backdoor access via dynamic proxy"

// 检测回调调用
from Class c, MethodAccess ma4
where ma4.getDeclaringType().equals(c)
and ma4.getTarget().hasModifier("private")
and ma4.getTarget().hasModifier("static")
and ma4.getTarget().hasName("backdoor")
and exists(Invocation i |
  i.getArgument(0).getBase().equals(ma4)
)

select ma4.getTarget(), "Possible backdoor access via callback"

// 检测类加载器调用
from ClassLoader cl, Class c2, MethodAccess ma5
where cl.loadClass(c2.getName()).equals(c2)
and ma5.getDeclaringType().equals(c2)
and ma5.getTarget().hasModifier("private")
and ma5.getTarget().hasModifier("static")
and ma5.getTarget().hasName("backdoor")

select ma5.getTarget(), "Possible backdoor access via classloader"