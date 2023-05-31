// 查询3：检测Java中可能存在后门的网络连接
import java

class SocketConnection extends Expr {
  SocketConnection() {
    this.getType() instanceof TypeSocket
  }
}

from SocketConnection sc
where sc instanceof ClassInstanceExpr
select sc, sc.getFile(), sc.getLocation().getStartLine(), sc.getLocation().getEndLine()