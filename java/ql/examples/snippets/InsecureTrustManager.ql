/**
 * @name `TrustManager` that accepts all certificates
 * @description Trusting all certificates allows an attacker to perform a machine-in-the-middle attack.
 * @kind path-problem
 * @problem.severity error
 * @security-severity 7.5
 * @precision high
 * @id java/insecure-trustmanager
 * @tags security
 *       external/cwe/cwe-295
 */

import java
import semmle.code.java.dataflow.DataFlow
import semmle.code.java.security.InsecureTrustManagerQuery
import InsecureTrustManagerFlow::PathGraph

from InsecureTrustManagerFlow::PathNode source, InsecureTrustManagerFlow::PathNode sink
where InsecureTrustManagerFlow::flowPath(source, sink)
select sink.getNode().asExpr().getFile().getAbsolutePath()+"$$"+sink.getNode().asExpr().getFile().getLocation().getStartLine(),sink.getLocation().getFile().getAbsolutePath()+"$$"+sink.getLocation().getStartLine() ,sink, source, sink, "This uses $@, which is defined in $@ and trusts any certificate.",
  source, "TrustManager",
  source.getNode().asExpr().(ClassInstanceExpr).getConstructedType() as type, type.nestedName()
