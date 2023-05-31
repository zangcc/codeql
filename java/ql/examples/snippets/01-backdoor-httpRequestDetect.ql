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

// Find all methods that belong to an HTTP request class
class HttpRequestMethod extends Method {
  HttpRequestMethod() {
    this.getDeclaringType() instanceof HttpRequestClass
  }
}

// Find all calls to an HTTP request method
from MethodAccess ma
where ma.getMethod() instanceof HttpRequestMethod
select ma.getLocation().getFile().getAbsolutePath() +":" + ma.getLocation().getStartLine()+"  可能存在后门HTTP请求: "+ma
