// 查询5：检测Java中可能存在后门的动态加载类
import java

from ClassInstanceExpr cie, StringLiteral sl
where cie.getType() instanceof TypeURLClassLoader and
  cie.getArgument(0).(ArrayCreationExpr).getInit().(ArrayInit).getAnInit().(ClassInstanceExpr).getArgument(0) = sl and
  sl.getValue().regexpMatch(".*[a-zA-Z0-9]+\\.[a-zA-Z0-9]+\\.[a-zA-Z0-9]+\\.[a-zA-Z0-9]+.*")
select cie, "Possible backdoor dynamic class loading."
