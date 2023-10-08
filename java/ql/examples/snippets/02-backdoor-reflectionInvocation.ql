// 查询2：检测Java中可能存在后门的反射调用
import java

from MethodAccess ma, ClassInstanceExpr cie
where ma.getMethod().hasName("invoke") and
  ma.getMethod().getDeclaringType() instanceof RefType and
  ma.getArgument(0) = cie and
  cie.getType() instanceof TypeRuntime and
  cie.getArgument(0).(StringLiteral).getValue().regexpMatch(".*[a-zA-Z0-9]+.*")
select ma,ma.getLocation().getFile().getAbsolutePath()+"$$"+ma.getLocation().getStartLine(), "Possible backdoor reflection invocation."



