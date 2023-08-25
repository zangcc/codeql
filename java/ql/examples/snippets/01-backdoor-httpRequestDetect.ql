import java

// Find all classes that extend or implement a class or interface related to HTTP requests
class HttpRequestClass extends RefType {
  HttpRequestClass() {
    this.getASupertype*().hasQualifiedName("java.net", "HttpURLConnection") or
    this.getASupertype*().hasQualifiedName("java.net", "URL") or
    this.getASupertype*().hasQualifiedName("org.apache.http", "HttpRequest") or
    this.getASupertype*().hasQualifiedName("org.apache.http.client", "HttpClient")
  }
}

string domainOrIpRegex() {
  result = "(^(?:\\d{1,3}\\.){3}\\d{1,3})" or 
  result = "^https?://" or 
  result = "^[\\w\\.]+\\.[a-z]{2,10}"
}


// Find all methods that belong to an HTTP request class
class HttpRequestMethod extends Method {
  HttpRequestMethod() {
    this.getDeclaringType() instanceof HttpRequestClass
  }
}

// Find all calls to an HTTP request method
from MethodAccess ma,StringLiteral sl,Variable var
where ma.getMethod() instanceof HttpRequestMethod 
  and ma.getAnArgument() = sl and  sl.getValue().regexpMatch(domainOrIpRegex()) 
  or ma.getAnArgument() = var.getAnAssignedValue() and  var.getAnAssignedValue().toString().regexpMatch(domainOrIpRegex()) 
select ma.getLocation().getFile().getAbsolutePath() +"$$" + ma.getLocation().getStartLine()+" 可能存在向"+ma.getAnArgument().toString()+"的后门HTTP请求: " +ma
