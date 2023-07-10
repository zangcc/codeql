/**
 * @name Access Java object methods through JavaScript exposure
 * @id java/android/webview-addjavascriptinterface
 * @description Exposing a Java object in a WebView with a JavaScript interface can lead to malicious JavaScript controlling the application.
 * @kind problem
 * @problem.severity warning
 * @security-severity 6.1
 * @precision medium
 * @tags security
 *       external/cwe/cwe-079
 */

import java
import semmle.code.java.frameworks.android.WebView

from MethodAccess ma
where ma.getMethod() instanceof WebViewAddJavascriptInterfaceMethod
select ma,ma.getLocation().getFile().getAbsolutePath()+"$$"+ma.getLocation().getStartLine()+"-"+ ma.getLocation().getEndLine(), "JavaScript interface to Java object added in Android WebView."
