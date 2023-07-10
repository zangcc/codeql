//主要匹配一下这种情况可能包含敏感信息的情况
// API pa ra m.setChangeContent(JSON.writeJson(changeContent));
//APIparam.setAuditStatus(AuditorAuditStatusEnum.WAIT.getCode());
//APIparam.setStatus(StatusEnum.NOT_DELETED.getCode());
//log.error("插入APIparam错误失败。param:{}", APIparam);
//下面ma是setStatus，v是APIparam
import java

from MethodAccess ma, Variable v, MethodAccess logInfo,string loc

where ma.getQualifier() = v.getAnAccess()
  and ma.getMethod().toString().regexpMatch("(?i).*(set|update|change).*")
  and v.getName().toString().regexpMatch("(?i).*(key|password|secret|vault|arn|param|token|content|mail|ldap|record|response|request|uuid|result).*")
  and logInfo.getMethod().toString().regexpMatch("(?i).*\\b(error|log|info|trace|warn|debug)\\b.*")
  and v.getAnAccess() = logInfo.getAnArgument()
  and loc = logInfo.getLocation().getFile().getAbsolutePath() + "$$" + logInfo.getLocation().getStartLine()

select logInfo,logInfo.getQualifier().toString()+"."+logInfo.getCallee().toString()+"()","打印了可能存在敏感信息的变量: "+v.getAnAccess().toString(),loc
