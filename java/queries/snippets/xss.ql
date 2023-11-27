// 查询1：检测Java中可能存在后门的字符串连接
import java

from StringLiteral s1, StringLiteral s2
where s1.getEnclosingStmt() = s2.getEnclosingStmt() and
  s1.getValue().regexpMatch(".*[a-zA-Z0-9]+.*") and
  s2.getValue().regexpMatch(".*[a-zA-Z0-9]+.*")
select s1.getEnclosingStmt(), "Possible backdoor string concatenation."
