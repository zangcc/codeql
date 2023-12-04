/**
 * @name URL redirection from local source
 * @description URL redirection based on unvalidated user-input
 *              may cause redirection to malicious web sites.
 * @kind path-problem
 * @problem.severity recommendation
 * @security-severity 6.1
 * @precision medium
 * @id java/unvalidated-url-redirection-local
 * @tags security
 *       external/cwe/cwe-601
 */

import java
import semmle.code.java.security.UrlRedirectLocalQuery
import UrlRedirectLocalFlow::PathGraph

from UrlRedirectLocalFlow::PathNode source, UrlRedirectLocalFlow::PathNode sink
where UrlRedirectLocalFlow::flowPath(source, sink)
select sink.getNode().getLocation().getFile().getAbsolutePath()+"$$"+sink.getNode().getLocation().getStartLine(),sink.getNode(), source, sink, "Untrusted URL redirection depends on a $@.", source.getNode(),
  "user-provided value"
