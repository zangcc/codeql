// 查询1：检测Java中可能存在后门的字符串连接
import java

from StringLiteral s1, StringLiteral s2
where s1.getEnclosingStmt() = s2.getEnclosingStmt() and
  // 限制字符串长度为10以上，以减少不必要的匹配
  s1.getValue().length() > 10 and s2.getValue().length() > 10 and
  // 使用更严格的正则表达式，以排除一些常见的字符串连接
  s1.getValue().regexpMatch(".*[a-zA-Z0-9]{5}.*") and
  s2.getValue().regexpMatch(".*[a-zA-Z0-9]{5}.*") and
  // 排除一些常用的API地址或者域名前缀
  not (s1.getValue().matches("https://api.%") or 
       s2.getValue().matches("https://api.%") or 
       s1.getValue().matches("http://%") or 
       s2.getValue().matches("http://%"))
select s1.getEnclosingStmt(), "Possible backdoor string concatenation."