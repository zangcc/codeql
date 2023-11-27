// import java
// import semmle.code.java.dataflow.DataFlow

// class LoggingCall extends MethodAccess {
//   LoggingCall() {
//     this.getMethod().getName().regexpMatch(".*info")
//   }
// }


// from LoggingCall lc
// select lc,"Possible print sensitve parameters: \""