// 查询4：检测Java中可能存在后门的文件操作
import java

from FileCreation fc, StringLiteral sl
where fc.getFileName() = sl and 
  sl.getValue().regexpMatch(".*[a-zA-Z0-9]+\\.[a-zA-Z0-9]+.*")
select fc, "Possible backdoor file operation."