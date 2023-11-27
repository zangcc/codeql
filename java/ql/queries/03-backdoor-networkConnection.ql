// 查询3：检测Java中可能存在后门的网络连接
import java

from SocketCreation sc, StringLiteral sl
where sc.getHost() = sl and 
  sl.getValue().regexpMatch(".*[a-zA-Z0-9]+\\.[a-zA-Z0-9]+\\.[a-zA-Z0-9]+\\.[a-zA-Z0-9]+.*")
select sc, "Possible backdoor network connection."