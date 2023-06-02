import javascript // 导入JavaScript的codeql库

from CallExpr call, string tempStr, string loc // 定义三个变量，分别是调用表达式，临时字符串和位置
where
  // 调用了 error(), INFO()函数，但不是console.log()
  call.getCalleeName().regexpMatch("(?i)\\b(error|log|info|trace|debug)\\b") and // 判断调用的函数名是否匹配正则表达式，忽略大小写
  not (call.getCallee() instanceof DotExpr and call.getCallee().(DotExpr).getBase().toString() = "console") and // 判断调用的函数是否是console.log()
  // 循环判断每个参数是否包含敏感词
  exists(int i | i in [0 .. call.getNumArgument() - 1] | // 遍历每个参数的索引
    call.getArgument(i).toString().regexpMatch("(?i).*\\b(key|password|secret|vault|arn|text|email|content|mail|ldap|message|response|request)\\b.*") and // 判断参数的字符串是否匹配正则表达式，忽略大小写
    not call.getArgument(i) instanceof StringLiteral and // 判断参数是否是字符串字面量
    tempStr = call.getArgument(i).toString()) and // 把参数的字符串赋值给临时字符串变量
  // 获取调用的位置
  loc = call.getLocation().getFile().getAbsolutePath() + ":" + call.getLocation().getStartLine() // 把调用的文件路径和行号赋值给位置变量

select call.getCallee().toString() + "()","打印了可能存在敏感信息的变量: "+tempStr, " "+loc // 输出调用的函数名，打印的敏感信息变量和位置
