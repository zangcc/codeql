import java

from MethodAccess ma
where
  // execute external command
  ma.getMethod().hasName("exec") and
  ma.getMethod().getDeclaringType().hasQualifiedName("java.lang", "Runtime")
  or
  // load dynamic library
  ma.getMethod().hasName("load") and
  ma.getMethod().getDeclaringType().hasQualifiedName("java.lang", "System")
  or
  // invoke method reflectively
  ma.getMethod().hasName("invoke") and
  ma.getMethod().getDeclaringType().hasQualifiedName("java.lang.reflect", "Method")
  or
  // create socket connection
  ma.getMethod().hasName("Socket") and
  ma.getMethod().getDeclaringType().hasQualifiedName("java.net", "Socket")
select ma.getLocation().getFile().getAbsolutePath() +"$$" + ma.getLocation().getStartLine()+"  可能存在后门: "+ma
