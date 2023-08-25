import javascript
// 定义一个正则表达式，用来匹配域名或者IP地址
// 例如： https://www.baiducin.con     www.example.com, 192.168.0.1, [2001:db8::1]
string domainOrIpRegex() {
   result = "(^(?:\\d{1,3}\\.){3}\\d{1,3})" or 
   result = "^https?://.*?" or 
   result = "^[\\w\\.]+\\.[a-z]{2,10}"
}

from  VarDecl var,string loc1
where  var.getStringValue().toString().regexpMatch(domainOrIpRegex()) and loc1 = var.getLocation().getFile().getAbsolutePath() +"$$" + var.getLocation().getStartLine()+ " 代码中出现了域名或者IP,请手工检查是否可能存在后门：" + var.getStringValue().toString() 

select loc1