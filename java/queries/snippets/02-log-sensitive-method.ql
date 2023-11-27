// 导入Java库
import java

// 定义一个类来表示log.info()或者log.error()方法调用
class LogMethod extends Method {
  LogMethod() {
    // 假设log对象是org.slf4j.Logger类型的
    this.getDeclaringType().hasQualifiedName("org.slf4j", "Logger") and
    // 只考虑info和error两种级别的日志
    this.hasName(["info", "error"])
  }
}

// 定义一个谓词来判断一个表达式是否包含了特定字符串"requestBody"
predicate containsKey(Expr e) {
  // 如果表达式是一个方法调用，并且方法名包含了"requestBody"
  e.(MethodAccess).getMethod().getName().toLowerCase().regexpMatch(".*?(?i)(response|currentTimeMillis|getTotalStats).*?")   // 调用函数比如request.toString() 
  and e.(MethodAccess).getMethod().getDeclaringType().getName().regexpMatch(".*?(?i)(apiinfo|geturi|request|nage|poolingHttpClientConnectionManager).*?") 
  // e.(ClassAccess).(MethodAccess).getMethod().getName().toLowerCase().regexpMatch(".*?(tostring).*?")
}

// 定义一个查询来找出所有满足条件的日志方法调用
// 定义一个查询来找出所有满足条件的日志方法调用
from LogMethod lm, MethodAccess ma, Expr arg
where ma.getMethod() = lm and // 方法调用对应于日志方法
arg = ma.getAnArgument() and // arg是方法调用的一个参数
containsKey(arg) // arg包含了特定字符串
select ma," 文件路径: " + ma.getLocation().getFile().getAbsolutePath() +":" + ma.getLocation().getStartLine()+"  Log里面打印了可能存在敏感信息的参数: "+ arg.toString()