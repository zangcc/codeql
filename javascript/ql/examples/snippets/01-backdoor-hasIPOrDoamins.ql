import javascript
// 定义一个正则表达式，用来匹配域名或者IP地址
// 例如： https://www.baiducin.con     www.example.com, 192.168.0.1, [2001:db8::1]
string domainOrIpRegex() {
   result = "(^(?:\\d{1,3}\\.){3}\\d{1,3})" or 
   result = "^https?" or 
   result = "^[\\w\\.]+\\.[a-z]{2,6}"
}

// 定义一个查询，用来查找代码中的函数调用，其参数是一个字符串字面量，其值可能是一个域名或者IP地址
from Function fc, ArgumentsVariable av
where fc.getArgumentsVariable() = av and  av.toString().regexpMatch(domainOrIpRegex()) 

select fc,fc.getLocation().getFile().getAbsolutePath() +"$$" + fc.getLocation().getStartLine(),"代码中出现了域名或者IP,请手工检查是否可能存在后门：" + fc.toString()
