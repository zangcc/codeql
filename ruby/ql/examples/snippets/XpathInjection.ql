/**
 * @name XPath query built from user-controlled sources
 * @description Building a XPath query from user-controlled sources is vulnerable to insertion of
 *              malicious XPath code by the user.
 * @kind path-problem
 * @problem.severity error
 * @security-severity 9.8
 * @precision high
 * @id rb/xpath-injection
 * @tags security
 *       external/cwe/cwe-643
 */

import codeql.ruby.DataFlow
import codeql.ruby.security.XpathInjectionQuery
import XpathInjection::PathGraph

from XpathInjection::PathNode source, XpathInjection::PathNode sink
where XpathInjection::flowPath(source, sink)
select sink.getNode().asExpr().getFile().getAbsolutePath()+"$$"+sink.getNode().asExpr().getFile().getLocation().getStartLine(),sink.getNode(), source, sink, "XPath expression depends on a $@.", source.getNode(),
  "user-provided value"
