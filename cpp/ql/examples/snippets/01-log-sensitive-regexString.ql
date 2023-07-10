import cpp

from FunctionCall fc,string str1
where
  fc.getTarget().toString().regexpMatch("(?i).*\\b(error|log|info|trace|warn|debug)\\b.*")
  and exists(int i , string s |
    not fc.getArgument(i) instanceof StringLiteral   and
    s = fc.getArgument(i).toString().trim()  and
    s.regexpMatch(".*(key|password|secret|vault|arn|param|token|content|mail|ldap|record|response|request|result).*")  and
    str1 = s
    )
   
select fc,"打印了可能存在敏感信息的变量:"+str1,fc.getLocation().getFile().getAbsolutePath() + "$$" + fc.getLocation().getStartLine().toString()


